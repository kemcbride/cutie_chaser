# an attempt at recreating stepmania's sm file parser.
# for these purposes, I really don't need to parse the steps. so I'll focus on NOT those.


def parse_sm(smfile_path):
    with open(smfile_path, 'r') as smfile:
        pass

# it looks like they have a file wrapper (surprise [eyeroll])
# that has a couple of helper functions.
# MsdFile is the type/class name
# GetNumValues() presumably reads the top level things, and counts how many are present
# #ARTIST:value; for example
# GetNumParams() presumably does the same thing except for the values within a value?
# Also has a getValue(i) function...

# so structure:
# for i in getNumValues()
#   getNumParams(i), params = GetValue(i)
#   sValueName = Rage::makeUpper(sParams[0]) # so this means it UPPERS the name, and gets it as a value...
#   then  there's a long case of which paramName it is I think... BGCHANGES, NOTES,
#   what else...
#   the rest seems to be covered by song_tag_helpers

# so of note is MsdFile as a class, and song_tag_helpers as a collection of helpers, i guess...
# Check this out: "The first field is typically an identifier, but it doesn't have to be."
# #PARAM0:PARAM1:PARAM2:PARAM3;
# #NEXTPARAM0:PARAM1:PARAM2:PARAM3;
# also check: "The semicolon is not optional, however if we hit a # on a newline, we'll recover."
# So fucntionally then, it is optional...
