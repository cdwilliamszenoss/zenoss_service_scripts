===============================================================================
ZenPacks.zenoss.PS.LogMonitor
===============================================================================

.. contents::
    :depth: 3

About
-------------------------------------------------------------------------------
ZenPack that monitors specified files (presumably log files) or directories for size or number of matches.

==================  ===========================================================
Prerequisite        Restriction
==================  ===========================================================
Product             Tested with Zenoss 5.1.7 and higher
Required ZenPacks   ``ZenPacks.zenoss.PythonCollector>=1.6.1``
                    ``ZenPacks.zenoss.Microsoft.Windows>=2.7.3``
Other dependencies  None
==================  ===========================================================

Modelers
--------

- LogMonitor.AdvancedLogSearches

The Log Search, Directory Search, and Size Check search components are manually added by the user as described in **Configuration and Usage**.

Advanced Log Searches are added upon device model based on entries in the zAdvancedLogSearches property.  For more information, see **Advanced Log Searches**

Installation / Usage / Removal
------------------------------

Install this ZenPack following the instructions in the Zenoss Resource Manager Admin Guide matching your Zenoss RM version.

Supported Operating Systems
---------------------------
* Windows
* AIX (SSH Only)
* Linux (SSH Only)
* Solaris (SSH Only) (Only Log Search, Directory Search, and Size Check supported on Solaris)

**Note:** Due to a limitation of the Windows FINDSTR utility, regular expression alternation is not supported when specifying a Search Pattern. This means you can not specify a list of patterns for which to search. You'd have to create multiple components to work around this. On UNIX devices you can specify multiple patterns on new lines.


Configuration and Usage
-----------------------

Log Search Component
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
To add a Log Search component, open the device in the web interface and select the corresponding option in the "+" button from the lower left.

Directory Search Component
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
To add a Directory Search component, open the device in the web interface and select the corresponding option in the "+" button from the lower left.

Size Check Component
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
To add a Size Check component, open the device in the web interface and select the corresponding optionin the "+" button from the lower left.

Advanced Log Searches
---------------------------------------------------
Advanced Log Searches allow for more flexibility in log monitoring, including

* two types of searches - "String" search, to track number of occurrences of a pattern, and "DataPoint within String" search, which can use a regular expression to extract a number from a specific string
* Search only from the last position read
* Graph and threshold based on the number of matches


Configuration Properties
~~~~~~~~~~~~~~~~~~~~~~~~
zAdvancedLogSearches
####################
This is the main zProperty for Advanced Log Searches.  When you edit this property, a special edit dialog will pop up that allows you to add and edit advanced log searches.

=================== ===============================
Search Type         Select "string" for a standard string search or "datapoint within string" to pull a datapoint out of the last occurrence of a string (ex. "There are 4 hung threads" - 4 being the datapoint you want
Search name         A unique name for each log search component
Log file            The log file to be searched (include full path)
Search Pattern      A regular expression or quoted string for the search.  See the **String Search** and **DataPoint within String Search** section for more details on OS-specific instructions
Clear/Zero Pattern  **Datapoint Search Only** This field is not required, but if included, the search will look for a specific string that, when found, will cause the search to return a datapoint of 0.  For example, if you had "There are 4 hung threads", then the datapoint would remain "4" until this pattern (e.g. "All hung threads clear") was found, at which point 0 would be returned
Test String         You can enter a copy of a line in your destination log file to see if the search or clear/zero pattern you have entered works
=================== ==============================

The following steps must be followed to enter and save the log searches:
1) Enter information in the fields
2) Click "Add", or "Update" (if editing an existing search)
3) **IMPORTANT** Your new or updated search has not been saved until you click "Submit" to update the zAdvancedLogSearchesProperty
4) After you have clicked "Submit", you need to either remodel the device or wait until the next modeling cycle for the Advanced Log Search components to appear

zLogSearchMaximumSizeInMB
#########################
If a log file in a search is larger than the specified size (in megabytes), the search will not be performed and a warning event will be generated

zLogSearchTimeout
#################
In Seconds.  If a log search takes longer than the specified number of seconds to return with data, the data is still stored, but a warning event will be generated informing of how long the search took.  Default is set to a low number, as most searches should come back quickly, but a good rule of thumb is to set it to slightly shorter than the cycle time to guarantee that searches aren't stepping on each other.

** THE FOLLOWING ZPROPERTIES ARE CURRENTLY ONLY IN USE FOR WINDOWS SEARCHES **
zLogSearchSleepAfterLines, zLogSearchSleepMilliseconds
######################################################
These two properties work together to help mitigate a performance hit on the Windows server.  As the search goes line by line through the log file, the script can be set to pause every "*zLogSearchSleepAfterLines*" lines, for "*zLogSearchSleepMilliseconds*" milliseconds.  Default is set to 1ms/2500 lines.  


String Search
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Linux
#####
Linux string searches are performed using grep with the switches -P (use Perl regular expression syntax) and -c (suppress normal output; instead print a count of matching lines).

The command used by Linux to do the search is this:

  ``grep -cP SEARCH_PATTERN LOGFILE_NAME``

Anything that you enter into the "search pattern" field in the Advanced Log Searches dialog must be able to be substituted for SEARCH_PATTERN in the command above.  So, for example, if you are only searching for one word, the following would work:

  Search pattern: ``Error``

  Test command: ``grep -cP Error some_logfile.log``

Or a regular expression without spaces:

  Search pattern: ``[0-9]+$`` (a pattern that will search for a line that has a number at the end of the line)

  Test command: ``grep -cP [0-9]+$ some_logfile.log``

But if you are searching for a string with spaces, you would need to enclose it in quotes:

  Search pattern: ``"Error detected"``

  Test command: ``grep -cP "Error detected" some_logfile.log``

Or if you are searching for a string with double-quotes, you could enclose it in single quotes:

  Search pattern: ``'Error code "12345" has been found'``

  Test command: ``grep -cP 'Error code "12345" has been found' some_logfile.log``

Keep in mind that everything in the search pattern will be evaluated as a regular expression, so if you are searching for any characters that are used in regular expressions, they will need to be escaped using a backslash.

Here are some examples:

  ====================================  ===========================================================
  Search for:                           Search Pattern:
  ====================================  ===========================================================
  Error                                 ``Error``
  Error detected                        ``Error detected``
  I've got a single quote               ``"I've got a single quote"``
  Here are some "double" quotes         ``'Here are some "double" quotes'``
  [ERROR] There has been an error       ``"\[ERROR\] There has been an error"``
  (Any line ending with a digit)        ``\d+$``
  ====================================  ===========================================================


AIX
#####
AIX string searches are performed using egrep with the switch -c (suppress normal output; instead print a count of matching lines).

The command used by AIX to do the search is this:

  ``egrep -c SEARCH_PATTERN LOGFILE_NAME``

Anything that you enter into the "search pattern" field in the Advanced Log Searches dialog must be able to be substituted for SEARCH_PATTERN in the command above.  So, for example, if you are only searching for one word, the following would work:

  Search pattern: ``Error``

  Test command: ``egrep -c Error some_logfile.log``

Or a regular expression without spaces:

  Search pattern: ``[0-9]+$`` (a pattern that will search for a line that has a number at the end of the line)

  Test command: ``egrep -c [0-9]+$ some_logfile.log``

But if you are searching for a string with spaces, you would need to enclose it in quotes:

  Search pattern: ``"Error detected"``

  Test command: ``egrep -c "Error detected" some_logfile.log``

Or if you are searching for a string with double-quotes, you could enclose it in single quotes:

  Search pattern: ``'Error code "12345" has been found'``

  Test command: ``egrep -c 'Error code "12345" has been found' some_logfile.log``

Keep in mind that everything in the search pattern will be evaluated as a regular expression, so if you are searching for any characters that are used in regular expressions, they will need to be escaped using a backslash.

Here are some examples:

  ====================================  ===========================================================
  Search for:                           Search Pattern:
  ====================================  ===========================================================
  Error                                 ``Error``
  Error detected                        ``"Error detected"``
  I've got a single quote               ``"I've got a single quote"``
  Here are some "double" quotes         ``'Here are some "double" quotes'``
  [ERROR] There has been an error       ``"\[ERROR\] There has been an error"``
  (Any line ending with a digit)          ``[0-9]+$``
  ====================================  ===========================================================

Windows
#######
Windows string searches are performed by using System.Text.RegularExpressions.Regex(SEARCH_PATTERN), comparing it to the log file, line by line from the last position read, and generating a count of matching lines.

The following is a stripped down version of the PowerShell commands used to generate a string count, and can be used to test your search patterns, replacing LOG_FILE with the log file to search and SEARCH_PATTERN with the pattern you are testing::

  $logfile = 'LOG_FILE';
  $pattern = 'SEARCH_PATTERN';
  $stream = New-Object System.IO.FileStream -ArgumentList $logfile, 'Open', 'Read', 'ReadWrite' -ErrorAction Stop;
  $reader = New-Object System.IO.StreamReader -ArgumentList $stream, $true;
  $reader.BaseStream.Seek(0, 'Begin') | Out-Null;
  $reader.ReadLine() | Out-Null;
  $reader.DiscardBufferedData();
  $regex = New-Object System.Text.RegularExpressions.Regex($pattern);
  $search_count = 0;
  while($null -ne ($buffer = $reader.ReadLine())) { if($regex.IsMatch($buffer)) { $search_count++; } }
  $reader.Close();
  $stream.Close();
  $search_count

Anything that you enter into the "search pattern" field in the Advanced Log Searches dialog must be able to be substituted for SEARCH_PATTERN in the command above.  So, unlike in Linux, quotes are NOT required in your search pattern, even if there are spaces or special characters in the pattern.  To escape a single quote, double it ('').  No escaping is required for double quotes.

Keep in mind that everything in the search pattern will be evaluated as a regular expression, so if you are searching for any characters that are used in regular expressions, they will need to be escaped using a backslash.

Here are some examples:

  ====================================  ===========================================================
  Search for:                           Search Pattern:
  ====================================  ===========================================================
  Error                                 ``Error``
  Error detected                        ``Error detected``
  I've got a single quote               ``I''ve got a single quote``
  Here are some "double" quotes         ``Here are some "double" quotes``
  [ERROR] There has been an error       ``\[ERROR\] There has been an error``
  (Any line ending with a digit)          ``\d+$``
  ====================================  ===========================================================


DataPoint within String Search
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"Datapoint within string" search requires a regular expression to extract a number from the matching string.  Due to differences in operating system implementation, different patterns must be used.

Linux
#####
Linux datapoint searches are performed using grep with the switches -P (use Perl regular expression syntax) and -o (print only the matched part of a matching line).

The command used by Linux to do the search is this:

``grep -oP SEARCH_PATTERN LOGFILE_NAME``

This command will give you ALL matching results, while the LogMonitor ZenPack will only return the last one found, but it will let you know if your search pattern returns what you are expecting.

Anything that you enter into the "search pattern" field in the Advanced Log Searches dialog must be able to be substituted for SEARCH_PATTERN in the command above.

The recommended way to do a datapoint search in Linux is to use **lookarounds** and the **digit character**.

``(?=sometext)`` - Lookahead: "sometext" comes immediately after the current position

``(?<=sometext)`` - Lookbehind: "sometext" comes immediately before the current position

``(?!sometext)`` - Negative lookahead: "sometext" definitely does NOT come immediately after the current position

``(?<!sometext)`` - Negative lookbehind: "sometext" definitely does NOT come immediately before the current position

For example, assuming a logfile ``some_logfile.log`` with the following entry:

 ``WSVR0605W: Thread “WebContainer : 1” has been active for 612,000 milliseconds and may be hung. There are 3 threads in total in the server that may be hung.``

A good search pattern to pull out the number of possible hung threads might be:

``'(?<=There are )\d+(?= threads in total in the server that may be hung.)'``

And you could test that on the command line as follows:

``grep -oP '(?<=There are )\d+(?= threads in total in the server that may be hung.)' some_logfile.log``

Which should return:

``3``

Some things to notice about this pattern:

- The significant piece here is the ``\d+``.  With grep -o, the lookahead and lookbehind will NOT be included, and only the digits in between will be returned

- If we are using lookaround syntax, we need to enclose the expression in single or double quotes.  Otherwise, we will get a syntax error for the unexpected ``(``.

AIX
###
AIX datapoint searches use a combination of egrep and sed.

The AIX method for datapoint searches has several idiosyncracies:

- For digits, since we cannot use Perl regular expressions, character class must be used, followed by an asterisk:  [0-9]*

- Lookaround logic does not work; you must use a "capturing group" to extract the number

- In regular expressions, a capturing group is indicated using ().  HOWEVER, because egrep and sed have different ways that parentheses need to be escaped, search patterns entered into the Log Monitoring ZenPack use DOUBLE parentheses (())to indicate a capturing group.  If a parenthesis is part of the text you're searching, it just needs to be escaped normally.   \\(

- The search pattern must compensate for the entire line; anything not explicitly covered by the regular expression will be returned with the datapoint.  So make sure to precede your search pattern with ^.* (any number of occurrences of any characters at the beginning of the line) and succeed your search pattern with .*$ (any number of occurrences of any characters at the end of the line)

The commands you can use to test your search pattern in AIX are:

1) egrep  'EGREP_SEARCH_PATTERN' LOG_FILE | sed -n -e 's/SED_SEARCH_PATTERN/\\1/p' | tail -1

OR

2) egrep  "EGREP_SEARCH_PATTERN" LOG_FILE | sed -n -e "s/SED_SEARCH_PATTERN/\\1/p" | tail -1

Use #2 only if your search pattern includes double quotes.  #1 should be used in all other circumstances.

Also notice that we have EGREP_SEARCH_PATTERN and SED_SEARCH_PATTERN.  This is due to the different ways egrep and sed use capturing groups, as mentioned above.  Because of these idiosyncracies, we have to take the search pattern that we are entering into the LogMonitor ZenPack and format it differently for each command.

For example, assuming a logfile ``some_logfile.log`` with the following entry:

 ``WSVR0605W: Thread "WebContainer : 1" has been active for 612,000 milliseconds and may be hung. There are 3 threads (total) in the server that may be hung.``

a good search pattern to pull out the number of possible hung threads might be:

 ``^.*There are (([0-9]*)) threads \(total\) in the server that may be hung.*$``

Take note that we have used (()) for our capturing group and backslashes to escape the parentheses in the actual text.  So, to test the command, we'll need to format the egrep and sed search patterns as follows

  ====================  ===============================================================================  ==================================================================================================
  Pattern:              New format:                                                                      What we changed:
  ====================  ===============================================================================  ==================================================================================================
  EGREP_SEARCH_PATTERN  ``^.*There are ([0-9]*) threads \(total\) in the server that may be hung.*$``    Double parentheses replaced with single
  SED_SEARCH_PATTERN    ``^.*There are \([0-9]*]\) threads (total) in the server that may be hung.*$``   Double parentheses replaced with escaped parentheses, backslashes removed from escaped parentheses
  ====================  ===============================================================================  ==================================================================================================

Now we can test our search on the command line as follows:

``egrep '^.*There are ([0-9]*) threads \(total\) in the server that may be hung.*$' some_logfile.log | sed -n -e 's/^.*There are \([0-9]*\) threads (total) in the server that may be hung.*$/\1/p' | tail -1``

Which should return:

``3``

Here are some example patterns:

  ============================================  ========  ================================================================
  Search for:                                   Expected  Search Pattern:
  ============================================  ========  ================================================================
  There are 3 hung threads                      3         ``^.*There are (([0-9]*)) hung threads.*$``
  A "double" quote datapoint: 31                31        ``^.*A "double" quote datapoint: (([0-9]*)).*$``
  [ERROR] 13 errors found                       13        ``^.*\[ERROR\] (([0-9]*)) errors found.*$``
  A parenthesis (is) here: 47 is the datapoint  47        ``^.*A parenthesis \(is\) here: (([0-9]*)) is the datapoint.*$``
  ============================================  ========  ================================================================

Windows
#######
Datapoint searches in Windows also use the System.Text.RegularExpressions object, as in the "string" search above.  However, to just test your search pattern, you can use this simpler command, replacing TEST_STRING with a line to test against, and SEARCH_PATTERN with your pattern::

  $matches = ''; $found = 'TEST_STRING' -match 'SEARCH_PATTERN'; $matches[0]

Anything that you enter into the "search pattern" field in the Advanced Log Searches dialog must be able to be substituted for SEARCH_PATTERN in the command above.

The recommended way to do a datapoint search in Windows is to use **lookarounds** and the **digit character**.

``(?=sometext)`` - Lookahead: "sometext" comes immediately after the current position

``(?<=sometext)`` - Lookbehind: "sometext" comes immediately before the current position

``(?!sometext)`` - Negative lookahead: "sometext" definitely does NOT come immediately after the current position

``(?<!sometext)`` - Negative lookbehind: "sometext" definitely does NOT come immediately before the current position

For example, for a log entry that looks like this:

 ``WSVR0605W: Thread “WebContainer : 1” has been active for 612,000 milliseconds and may be hung. There are 3 threads in total in the server that may be hung.``

A good search pattern to pull out the number of possible hung threads might be:

  ``(?<=There are )\d+(?= threads in total in the server that may be hung.)``

And you could test that on the command line as follows:

  ``$matches = ''; $found = 'WSVR0605W: Thread “WebContainer : 1” has been active for 612,000 milliseconds and may be hung. There are 3 threads in total in the server that may be hung.' -match '(?<=There are )\d+(?= threads in total in the server that may be hung.)'; $matches[0]``

Which should return:
   ``3``

The significant piece here is the ``\d+``.  With System.Text.RegularExpressions, lookahead and lookbehind will NOT be included, and only the digits in between will be returned

For datapoint regular expressions, double-quotes do NOT need to be escaped.  Single quotes DO need to be escaped by doubling, and other special characters that are used in regular expressions must be escaped by a backslash.

Here are some example patterns:

  ====================================  ==================  ===========================================================
  Search for:                           Expected Datapoint  Search Pattern:
  ====================================  ==================  ===========================================================
  There are 3 hung threads              3                   ``(?<=There are )\d+(?= hung threads)``
  I'm a single quote datapoint: 25      25                  ``(?<=I''m a single quote datapoint: )\d+``
  A "double" quote datapoint: 31        31                  ``(?<=A "double" quote datapoint: )\d+``
  [ERROR] 13 errors found               13                  ``(?<=\[ERROR\] )\d+(?= errors found)``
  ====================================  ==================  ===========================================================



Changelog
---------

- 1.3.0

  - Add component to max size event.
  - Fix usage of search_patterns property on RM 6.2

