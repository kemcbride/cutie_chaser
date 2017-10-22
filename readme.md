<p align="center"><img src="https://remywiki.com/images/f/fa/CUTIE_CHASER_banner_old.png"></p>

Note: this is specifically for stepmania/openITG.

Sometimes I want to listen to music of packs for fun, and looking up the
tracks one by one can be annoying.

idea: create youtube playlists based on packs - that way when you want to check out a pack
but for some reason don't have access to stepmania/itg on hand (idk, browsing r21freak on mobile)
you can just search up a playlist (in an ideal world)

Often when I hear stuff in a pack, it's music I don't know.


## Technically Speaking

All it does is hop onto the youtube API and do a search using the metadata
specified in the .sm file and grab the first result. So yeah, it can TOTALLY be wrong.

But usually it's not.

Check these out, for example:

[Animusic Season 1](https://www.youtube.com/watch?v=5KDltB4AvoY&list=PL_B30pn44WOVuiAsWCWGgf2mA-153un7G)
- two errors as far as I can tell, out of 41 tracks?

[Ninjafar's Insanely Cute Electronic Simfile Troop](https://www.youtube.com/playlist?list=PL_B30pn44WOUthLP-d-4pgMGPkls-txgt)
- no errors as far as I can tell, out of 12 tracks?


## More Technically Speaking

Check out these reference links for parsing sm files
(and analogously per the different NoteLoader files)

- https://github.com/stepmania/stepmania/blob/master/src/MsdFile.cpp
- https://github.com/stepmania/stepmania/blob/master/src/NotesLoaderSM.cpp
