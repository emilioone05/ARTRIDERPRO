from rest_framework import serializers
from .models import Review
from reservations.models import Reserva

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['autor']

    def validate(self, data):
        # F-601: Validar que la reserva esté FINALIZADA antes de dejar review
        reserva = data['reserva']
        if reserva.estado != 'FINALIZADO':
            raise serializers.ValidationError("Solo puedes reseñar reservas finalizadas.")
        return data