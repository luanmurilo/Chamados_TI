from django.core.mail import EmailMessage
from django.core.mail import mailers

from ..models import ConfiguracaoEmail


def obter_configuracao_email():
    """
    Retorna a configuração de e-mail ativa.
    """

    return ConfiguracaoEmail.objects.filter(
        ativo=True
    ).first()


def configurar_mailer(configuracao):
    """
    Configura o mailer padrão do Django utilizando
    os dados armazenados no banco.
    """

    mailer = mailers['default']

    mailer.host = configuracao.servidor_smtp
    mailer.port = configuracao.porta_smtp
    mailer.username = configuracao.usuario_smtp
    mailer.password = configuracao.senha_smtp

    mailer.use_tls = configuracao.usar_tls
    mailer.use_ssl = configuracao.usar_ssl

    mailer.timeout = None

    return mailer


def enviar_email(
    destinatarios,
    assunto,
    mensagem,
):
    """
    Envia um e-mail utilizando a configuração SMTP
    cadastrada no banco.
    """

    configuracao = obter_configuracao_email()

    if not configuracao:
        raise ValueError(
            'Nenhuma configuração de e-mail ativa foi encontrada.'
        )

    if isinstance(destinatarios, str):
        destinatarios = [destinatarios]

    mailer = configurar_mailer(configuracao)

    email = EmailMessage(
        subject=assunto,
        body=mensagem,
        from_email=(
            f'{configuracao.nome_remetente} '
            f'<{configuracao.email_remetente}>'
        ),
        to=destinatarios,
    )

    if not mailer.open():
        raise ConnectionError(
            'Não foi possível estabelecer conexão com o servidor SMTP.'
        )

    try:

        return mailer.send_messages(
            [email]
        )

    finally:

        mailer.close()