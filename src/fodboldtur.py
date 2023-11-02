import os
from colorama import Fore
import pickle

total_pay = 4500


def load_list() -> dict[str, float]:
    infile = open('../betalinger.pk', 'rb')
    fodboldtur = pickle.load(infile)
    infile.close()

    return fodboldtur


def payment(people: dict, arguments: list):
    name = arguments[1] + " " + arguments[2]
    try:
        amount = arguments[3]
        amount = float(amount)

    except ValueError:
        print('ikke et heltal')
        return

    print('tilføjede {} penge til {}s konto'.format(amount, name))
    # Create new name
    if name not in people.keys():
        people[name] = amount
        return

    people[name] += amount


def remove_name(people: dict, arguments: list):
    name = arguments[1] + " " + arguments[2]

    if name not in people.keys():
        print('Dette navn er ikke gyldigt')
        return

    del people[name]
    print('fjernede {} fra turen'.format(name))


def save_list(people):
    outfile = open('../betalinger.pk', 'wb')
    pickle.dump(people, outfile)
    outfile.close()


def printliste(people):
    individual_pay = total_pay / len(people)
    for key, value in people.items():
        print(f'{key} har betalt: {value} og mangler at betale: {individual_pay - value}')

    print(f'I alt betalt: {sum(people.values())}, mangler: {total_pay - sum(people.values())}\n')


def print_people(people: dict, arguments: list, isRich=False):
    sorted_dict = sorted(people.items(), key=lambda v: v[1], reverse=isRich)
    try:
        print_amount = min(int(arguments[1]), len(sorted_dict))
    except ValueError:
        print('Ikke odenlig talværdi givet')
        return

    for i in range(print_amount):
        print(sorted_dict[i])


def print_help():
    print("   --------------------------------------------------------")
    print("{}    list:{} Print liste af mennesker\n".format(Fore.LIGHTYELLOW_EX, Fore.WHITE))
    print("{}    betal <fornavn> <efternavn> <mængde>:{} Betal en mængde penge\n".format(Fore.LIGHTYELLOW_EX, Fore.WHITE))
    print("{}    fjern <fornavn> <efternavn>:{} fjern medlem og hans penge\n".format(Fore.LIGHTYELLOW_EX, Fore.WHITE))
    print("{}    bund <nummer>:{} Print de <nummer> der mangler at betale mest\n".format(Fore.LIGHTYELLOW_EX, Fore.WHITE))
    print("{}    top <nummer>:{} Print de <nummer> der har betalt mest\n".format(Fore.LIGHTYELLOW_EX, Fore.WHITE))
    print("{}    clear | cls:{} sletter alt tekst i terminalen\n".format(Fore.LIGHTYELLOW_EX, Fore.WHITE))
    print("{}    gem:{} gemmer programmet\n".format(Fore.LIGHTYELLOW_EX, Fore.WHITE))
    print("{}    autogem <sand/falsk>:{} slår autogem fra og til\n".format(Fore.LIGHTYELLOW_EX, Fore.WHITE))
    print("{}    slut:{} Stop program".format(Fore.LIGHTYELLOW_EX, Fore.WHITE))
    print("   --------------------------------------------------------\n")


def main():
    def wrong_arg_len(count: int) -> bool:
        if len(arguments) != count:
            print(f'{Fore.RED}Kommando bruger {count} argumenter, men du gav {len(arguments)}'
                  f'\n{Fore.YELLOW}Brug hjælp command til hjælp')
            return True
        return False

    print('\n#### INDE I DEN SUPER SEJE COMMAND PROMPT ####')
    print('######### LAVET TIL ET SKOLE PROJEKT #########\n')

    fodboldtur = load_list()
    auto_save = False

    while True:
        valg = input("{}> {}".format(Fore.WHITE, Fore.GREEN))

        if len(valg) == 0:
            continue

        print(Fore.WHITE)
        arguments = valg.split(" ")

        match arguments[0].lower():
            case 'hjælp':
                print_help()

            case 'list':
                if wrong_arg_len(1):
                    continue

                printliste(fodboldtur)

            case 'betal':
                if wrong_arg_len(4):
                    continue

                payment(fodboldtur, arguments)

            case 'fjern':
                if wrong_arg_len(3):
                    continue

                remove_name(fodboldtur, arguments)

            case 'bund':
                if wrong_arg_len(2):
                    continue

                print_people(fodboldtur, arguments)

            case 'top':
                if wrong_arg_len(2):
                    continue

                print_people(fodboldtur, arguments, True)

            case 'clear' | 'cls':
                os.system('cls')
                continue

            case 'autogem':
                if wrong_arg_len(2):
                    continue

                if arguments[1].lower() == 'true':
                    auto_save = True
                elif arguments[1].lower() == 'false':
                    auto_save = False

            case 'gem':
                save_list(fodboldtur)

            case 'slut':
                print('### PROGRAMMET ER LUKKET ###\n')
                break

            case _:
                print(f'{Fore.RED}\'{valg}\' er ikke en kommando brug kommandoen \'Hjælp\'\n')

        if auto_save:
            save_list(fodboldtur)


if __name__ == '__main__':
    main()
