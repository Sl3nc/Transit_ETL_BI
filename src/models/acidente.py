class FatoAcidente:
    def __init__(self, pk_acidente, fk_boletim, fk_contexto, fk_logradouro, quantidade_vitimas, indicador_fatalidade, numero_envolvidos):
        self.pk_acidente = pk_acidente
        self.fk_boletim = fk_boletim
        self.fk_contexto = fk_contexto
        self.fk_logradouro = fk_logradouro
        self.quantidade_vitimas = quantidade_vitimas
        self.indicador_fatalidade = indicador_fatalidade
        self.numero_envolvidos = numero_envolvidos
