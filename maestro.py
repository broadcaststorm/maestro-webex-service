#!/usr/bin/env python3

from webexteamssdk import Message


# TODO: Convert this hack to click or typer
def project_list():
    pass


def scenario_list():
    pass


supported_commands = {
    'project': {
        'list': project_list,
    },
    'scenario': {
        'list': scenario_list,
    }
}


def help():
    lines = []
    lines.append('Supported commands are:')

    for resource in supported_commands:
        for cmds in supported_commands[resource]:
            lines.append(
                f'\t{resource} {cmds} [args]'
            )

    return '\n'.join(lines)


def process_command_message(cmd_message: Message):
    """

    Process the command messages sent to the bot and received here via the
    Webex Teams webhook.

    :param webexteamssdk.Message cmd_message: The message obj to be processed
    :return: roomId, parentId, message for return message to the teams room.

    """

    # First word is the Bot name... for now, hardcode "Lab", splice it out
    words = cmd_message.text[3:].split()

    # Special case: help
    if words[0] == 'help':
        result = help()

        return (
            cmd_message.roomId,
            cmd_message.id,
            result,
        )

    # Pattern:  resource action arguments
    if words[0] not in supported_commands:
        error_message = f'Resource {words[0]} not recognized from: '
        error_message += str(cmd_message.text[3:])

        return (
            cmd_message.roomId,
            cmd_message.id,
            error_message
        )

    if len(words) == 1:
        error_message = f'No command provided for resource {words[0]}'

        return (
            cmd_message.roomId,
            cmd_message.id,
            error_message
        )

    if words[1] not in supported_commands[words[0]]:
        error_message = f'Command {words[1]} not recognized for resource {words[0]}'

        return (
            cmd_message.roomId,
            cmd_message.id,
            error_message
        )

    # Call the function pointed to by the dictionary
    command_parse = supported_commands[words[0]][words[1]]

    if len(words) > 2:
        command_parse(words[2:])
    else:
        command_parse()

    return (
        cmd_message.roomId,
        cmd_message.id,
        f'Received resource {words[0]} with cmd/args {words[1:]}'
    )
