from rest_framework import mixins, serializers, viewsets

from banks import models as bank_models
from programs import models as program_models


class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = bank_models.Bank
        fields = ["id", "name", "countries"]


class BankViewSet(viewsets.ModelViewSet):
    queryset = bank_models.Bank.objects.all()
    serializer_class = BankSerializer


class Transaction:
    def __init__(self, country, currency, program, bank, is_eligible=False):
        self.country = country
        self.currency = currency
        self.program = program
        self.bank = bank
        self.is_eligible = is_eligible


class TransactionSerializer(serializers.Serializer):
    country = serializers.CharField(max_length=10)
    currency = serializers.CharField(max_length=10)

    program = serializers.CharField(max_length=10)
    bank = serializers.CharField(max_length=10)

    is_eligible = serializers.BooleanField(default=False)

    def create(self, validated_data):
        return Transaction(**validated_data)

    def update(self, instance: Transaction, validated_data):
        instance.is_eligible = validated_data.get("is_eligible", False)
        return instance

    def validate(self, data):
        # TODO basic data type validation should be here
        return data


class TransactionViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
):
    serializer_class = TransactionSerializer

    def __init__(self, **kwargs):
        # TODO we could add here a layer which handles the DB logic/interaction/queries separately from the API logic
        # self.database_layer = MySingletonDbClass(...)
        super().__init__(**kwargs)

    def perform_create(self, serializer: serializers.Serializer):
        if self._is_program_and_currency_exists(self.request.data) and \
                self._is_bank_exists_in_country(self.request.data):
            serializer.save(is_eligible=True)
            return serializer

        serializer.save(is_eligible=False)
        return serializer

    @staticmethod
    def _is_program_and_currency_exists(request_data):
        program_name = request_data.get("program")
        currency = request_data.get("currency")
        # TODO this should be optimized, e.g adding filter,etc
        for program in program_models.Program.objects.all().iterator():
            if program_name == program.name and currency == program.currency:
                return True
        return False

    @staticmethod
    def _is_bank_exists_in_country(request_data):
        bank_name = request_data.get("bank")
        country = request_data.get("country")
        # TODO this should be optimized, e.g adding filter,etc
        for bank in bank_models.Bank.objects.all().iterator():
            if bank_name == bank.name and country in bank.countries:
                return True
        return False
