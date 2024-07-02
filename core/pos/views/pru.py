from datetime import datetime, timedelta

def current_time():
    return datetime.now().time()

def current_date():
    return datetime.now().date()

class RegistroSalida(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    hora_salida = models.TimeField(default=current_time)
    fecha = models.DateField(default=current_date)
    token = models.CharField(max_length=8)
    descripcion_actividad = models.TextField(verbose_name='Descripción de la Actividad', null=True, blank=True)
    total_horas = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name='Total de Horas Hechas')
    tiempo_extra = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name='Tiempo Extra')

    def save(self, *args, **kwargs):
        if not self.validate_token():
            raise ValueError("Token inválido")
        if not self.has_previous_entry():
            raise ValueError("No hay registro de entrada previo")
        self.calculate_hours()
        self.update_actividad_estado()
        super().save(*args, **kwargs)

    def validate_token(self):
        return self.token == self.alumno.token

    def has_previous_entry(self):
        return RegistroEntrada.objects.filter(alumno=self.alumno, fecha=self.fecha).exists()

    def calculate_hours(self):
        entrada = RegistroEntrada.objects.filter(alumno=self.alumno, fecha=self.fecha).first()
        if entrada:
            hentrada_dt = datetime.combine(self.fecha, entrada.hora_entrada)
            hsalida_dt = datetime.combine(self.fecha, self.hora_salida)
            delta = hsalida_dt - hentrada_dt
            total_horas = delta.total_seconds() / 3600  # Convertir segundos a horas

            # Verificar si es tiempo extra
            horario = Horario.objects.filter(alumno=self.alumno, dia=self.fecha.strftime('%A').upper()).first()
            if horario and horario.programado:
                hentrada_prog = datetime.combine(self.fecha, horario.hentrada)
                hsalida_prog = datetime.combine(self.fecha, horario.hsalida)
                extra_antes = (hentrada_prog - hentrada_dt).total_seconds() / 3600 if hentrada_dt < hentrada_prog else 0
                extra_despues = (hsalida_dt - hsalida_prog).total_seconds() / 3600 if hsalida_dt > hsalida_prog else 0
                tiempo_extra = extra_antes + extra_despues
            else:
                tiempo_extra = total_horas  # Todo el tiempo es extra si no es un día programado

            self.total_horas = round(total_horas, 2)
            self.tiempo_extra = round(tiempo_extra, 2)

    def update_actividad_estado(self):
        if not self.descripcion_actividad:
            self.descripcion_actividad = 'No hay actividades programadas'

    def format_hours_minutes(self, decimal_hours):
        hours = int(decimal_hours)
        minutes = int((decimal_hours - hours) * 60)
        return f'{hours} horas y {minutes} minutos'

    def toJSON(self):
        item = model_to_dict(self)
        item['alumno'] = self.alumno.toJSON()
        item['hora_salida'] = self.hora_salida.strftime('%H:%M')
        item['fecha'] = self.fecha.strftime('%Y-%m-%d')
        item['total_horas'] = self.format_hours_minutes(float(self.total_horas)) if self.total_horas else '0 horas y 0 minutos'
        item['tiempo_extra'] = self.format_hours_minutes(float(self.tiempo_extra)) if self.tiempo_extra else '0 horas y 0 minutos'
        item['descripcion_actividad'] = self.descripcion_actividad or 'No hay actividades programadas'
        return item

    class Meta:
        verbose_name = 'Salida'
        verbose_name_plural = 'Salidas'
