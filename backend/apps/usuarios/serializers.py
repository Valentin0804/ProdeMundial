from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import Usuario, GrupoPrivado, Miembro


class RegistroSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Usuario
        fields = ('username', 'email', 'password', 'password2', 'first_name', 'last_name')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': 'Las contraseñas no coinciden.'})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        usuario = Usuario.objects.create_user(**validated_data)
        return usuario


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'avatar', 'bio')
        read_only_fields = ('id',)


class GrupoPrivadoSerializer(serializers.ModelSerializer):
    admin = UsuarioSerializer(read_only=True)
    cantidad_miembros = serializers.SerializerMethodField()

    class Meta:
        model = GrupoPrivado
        fields = ('id', 'nombre', 'codigo_invitacion', 'admin',
                  'cantidad_miembros', 'creado_en')
        read_only_fields = ('id', 'codigo_invitacion', 'admin', 'creado_en')

    def get_cantidad_miembros(self, obj):
        return obj.miembros.count()

    def create(self, validated_data):
        validated_data['admin'] = self.context['request'].user
        return super().create(validated_data)


class MiembroSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer(read_only=True)

    class Meta:
        model = Miembro
        fields = ('id', 'usuario', 'fecha_union')
