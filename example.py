from filter import Pipeline, Filter, Operation, Clause, AND, OR, Option


def main():
    Pipeline([
        Filter(
            'Ignore',
            Operation(OR, [
                Clause('from:useless@words.com'),
                Operation(AND, [
                    Clause('from:noreply@spam.com'),
                    Clause('subject:"Advertisement"'),
                ]),
            ]),
            Option(apply_label=False, skip_inbox=True),
        ),
        Filter(
            'Alarm',
            Operation(OR, [
                Operation(AND, [
                    Clause('to:monitor@service.com'),
                    Clause('subject:Panic'),
                ]),
                Operation(AND, [
                    Clause('from:alert@dtdg.co'),
                ]),
                Clause('from:database@server.com'),
            ]),
        ),
        Filter(
            'Report',
            Operation(OR, [
                Clause('subject:News'),
                Clause('subject:"Weekly Report"'),
                Clause('to:rss@example.com'),
            ]),
        ),
        Filter(
            'Random',
            Clause('from:random@company.com'),
        ),
        Filter(
            'Company',
            Operation(OR, [
                Clause('to:engineer@example.com'),
                Clause('to:request@example.com'),
            ]),
        ),
    ]).save('output.xml')


main()

