# Pipelined Gmail Filter Generator

Filters in gmail are work independently. So it's really hard to filtering out mails sequentially. This tool helps you make gmail filters when....
> You have 100 mails 
> 
> Use the filter A and select 10 mails from 100 mails and give the label A
> 
> Use the filter B and select 10 mails from remaing 90 mails and give the label B
> 
> Use the filter C and select 10 mails from remaing 80 mails and give the label C
>
> ...
> 
> Select whole remaining mails and give the label "Others"


## How to use

It's pure python script. You don't need any installation 
step.

---

**example.py**
```python
from filter import Pipeline, Filter, Operation, Clause, AND, OR, Option


def main():
    Pipeline([
        Filter(
            "Ignore",
            Operation(OR, [
                Operation(AND, [
                    Clause("from:noreply@md.getsentry.com"),
                    Clause("subject:\"Advertisement\""),
                    Clause("subject:\"False Alarm\""),
                ]),
                Operation(OR, [
                    Clause("from:sam@example.com"),
                    Clause("cc:jiwon@example.com"),
                ]),
                Clause("from:noreply@lokalise.com"),
                Clause("to:cream@example.com"),
            ]),
            Option(apply_label=False, skip_inbox=True),
        ),
        Filter(
            "Alarm",
            Operation(OR, [
                Operation(AND, [
                    Clause("to:alarm@example.com"),
                    Clause("subject:ALARM"),
                ]),
                Operation(AND, [
                    Clause("from:alert@dtdg.co"),
                    Clause("to:monitor@md.getsentry.com"),
                ]),
                Clause("from:noreply@md.getsentry.com"),
            ]),
        ),
        Filter(
            "Report",
            Operation(OR, [
                Clause("subject:\"News\""),
                Clause("subject:\"Weekly Report\""),
                Clause("to:collector@example.com"),
            ]),
        ),
        Filter(
            "SE/Game",
            Clause("to:engineer+game@example.com"),
        ),
        Filter(
            "SE",
            Operation(OR, [
                Clause("to:engineer@example.com"),
                Clause("to:request@example.com"),
            ]),
        ),
        Filter(
            "example",
            Clause("from:@example.com"),
        ),
    ]).save("output.xml")


main()

```
**run**
```
$ python example.py

(...short information will be printed...)

done. go gmail and export output.xml.
```
**output.xml**
```xml
<?xml version="1.0" ?>
<feed xmlns="http://www.w3.org/2005/Atom" xmlns:apps="http://schemas.google.com/apps/2006">
	<title>Mail Filters</title>
	<entry>
		<category term="filter"/>
		<title>Mail Filters</title>
		<content/>
		<apps:property name="hasTheWord" value="(((from:noreply@md.getsentry.com AND subject:&quot;Advertisement&quot; AND subject:&quot;False Alarm&quot;) OR (from:sam@example.com OR cc:jiwon@example.com) OR from:noreply@lokalise.com OR to:cream@example.com))"/>
		<apps:property name="shouldArchive" value="true"/>
		<apps:property name="sizeOperator" value="s_sl"/>
		<apps:property name="sizeUnit" value="s_smb"/>
	</entry>
	<entry>
		<category term="filter"/>
		<title>Mail Filters</title>
		<content/>
		<apps:property name="hasTheWord" value="(((to:alarm@example.com AND subject:ALARM) OR (from:alert@dtdg.co AND to:monitor@md.getsentry.com) OR from:noreply@md.getsentry.com) AND ((-from:noreply@md.getsentry.com OR -subject:&quot;Advertisement&quot; OR -subject:&quot;False Alarm&quot;) AND (-from:sam@example.com AND -cc:jiwon@example.com) AND -from:noreply@lokalise.com AND -to:cream@example.com))"/>
		<apps:property name="label" value="Alarm"/>
		<apps:property name="sizeOperator" value="s_sl"/>
		<apps:property name="sizeUnit" value="s_smb"/>
	</entry>
	<entry>
		<category term="filter"/>
		<title>Mail Filters</title>
		<content/>
		<apps:property name="hasTheWord" value="((subject:&quot;News&quot; OR subject:&quot;Weekly Report&quot; OR to:collector@example.com) AND ((-from:noreply@md.getsentry.com OR -subject:&quot;Advertisement&quot; OR -subject:&quot;False Alarm&quot;) AND (-from:sam@example.com AND -cc:jiwon@example.com) AND -from:noreply@lokalise.com AND -to:cream@example.com) AND ((-to:alarm@example.com OR -subject:ALARM) AND (-from:alert@dtdg.co OR -to:monitor@md.getsentry.com) AND -from:noreply@md.getsentry.com))"/>
		<apps:property name="label" value="Report"/>
		<apps:property name="sizeOperator" value="s_sl"/>
		<apps:property name="sizeUnit" value="s_smb"/>
	</entry>
	<entry>
		<category term="filter"/>
		<title>Mail Filters</title>
		<content/>
		<apps:property name="hasTheWord" value="(to:engineer+game@example.com AND ((-from:noreply@md.getsentry.com OR -subject:&quot;Advertisement&quot; OR -subject:&quot;False Alarm&quot;) AND (-from:sam@example.com AND -cc:jiwon@example.com) AND -from:noreply@lokalise.com AND -to:cream@example.com) AND ((-to:alarm@example.com OR -subject:ALARM) AND (-from:alert@dtdg.co OR -to:monitor@md.getsentry.com) AND -from:noreply@md.getsentry.com) AND (-subject:&quot;News&quot; AND -subject:&quot;Weekly Report&quot; AND -to:collector@example.com))"/>
		<apps:property name="label" value="SE/Game"/>
		<apps:property name="sizeOperator" value="s_sl"/>
		<apps:property name="sizeUnit" value="s_smb"/>
	</entry>
	<entry>
		<category term="filter"/>
		<title>Mail Filters</title>
		<content/>
		<apps:property name="hasTheWord" value="((to:engineer@example.com OR to:request@example.com) AND ((-from:noreply@md.getsentry.com OR -subject:&quot;Advertisement&quot; OR -subject:&quot;False Alarm&quot;) AND (-from:sam@example.com AND -cc:jiwon@example.com) AND -from:noreply@lokalise.com AND -to:cream@example.com) AND ((-to:alarm@example.com OR -subject:ALARM) AND (-from:alert@dtdg.co OR -to:monitor@md.getsentry.com) AND -from:noreply@md.getsentry.com) AND (-subject:&quot;News&quot; AND -subject:&quot;Weekly Report&quot; AND -to:collector@example.com) AND -to:engineer+game@example.com)"/>
		<apps:property name="label" value="SE"/>
		<apps:property name="sizeOperator" value="s_sl"/>
		<apps:property name="sizeUnit" value="s_smb"/>
	</entry>
	<entry>
		<category term="filter"/>
		<title>Mail Filters</title>
		<content/>
		<apps:property name="hasTheWord" value="(from:@example.com AND ((-from:noreply@md.getsentry.com OR -subject:&quot;Advertisement&quot; OR -subject:&quot;False Alarm&quot;) AND (-from:sam@example.com AND -cc:jiwon@example.com) AND -from:noreply@lokalise.com AND -to:cream@example.com) AND ((-to:alarm@example.com OR -subject:ALARM) AND (-from:alert@dtdg.co OR -to:monitor@md.getsentry.com) AND -from:noreply@md.getsentry.com) AND (-subject:&quot;News&quot; AND -subject:&quot;Weekly Report&quot; AND -to:collector@example.com) AND -to:engineer+game@example.com AND (-to:engineer@example.com AND -to:request@example.com))"/>
		<apps:property name="label" value="example"/>
		<apps:property name="sizeOperator" value="s_sl"/>
		<apps:property name="sizeUnit" value="s_smb"/>
	</entry>
</feed>
```

---
Finally, import this file on the gmail filter settings.
