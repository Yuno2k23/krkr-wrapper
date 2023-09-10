# KiriKiri Wrapper

Some games made on older versions of KiriKiri don't support automatic word wrapping, and to solve this, the [Insani](http://www.insani.org/about.html) fansub created a tool that added word wrapping to Fate/stay night which, consequently,  works on some games made on KiriKiri.

I've added some modifications to the original tool, as you can see at the end of this document.

## Usage

### → Patching the game

Along with this tool comes 3 modified `.tjs` files:

- MessageLayer.tjs
- MainWindow.tjs
- HistoryLayer.tjs

You can place those files in `patch.xp3` and test it yourself.

If you're very lucky, it will work on first try, otherwise you have to modify the scripts comparing with the ones from the original game.  

In some cases, it's only necessary to change some variables and add some code from the original game.

> Tip: there are comments with `insani` to indicate the modified code snippets.

#

### → Processing the scene scripts

Open a terminal in the folder and use the command:

```properties
python krkr-wrapper.py {wrap, unwrap} <input_file> <output_file> [--input-encoding ENCODING] [--output-encoding ENCODING]
```

```properties
positional arguments:
  {wrap,unwrap}         Chooses between wrapping and unwrapping
  input_file            Path of the .ks file
  output_file           Path of the resulting .ks file

options:
  --input-encoding ENCODING, --ie ENCODING
                        Input file encoding, SHIFT-JIS by default
  --output-encoding ENCODING, --oe ENCODING
                        Output file encoding, SHIFT-JIS by default

  -h, --help            Help Message
```

If your language has accent marks and special characters, like Portuguese and Spanish, use UTF-16.

> The only encodings that work perfectly are SHIFT-JIS and UTF-16, UTF-8 may not work in some cases.

## Tested Games

- [Tsukihime PLUS+DISC](https://vndb.org/v49)
- [Ludesia Spidering with Scraping](https://vndb.org/v1814)
- [Until We Meet Again](https://vndb.org/v230)

> I didn't test with [Fate/stay night](https://vndb.org/v11), but it probably works...
  
If you managed to make it work on another game, let me know so I can update this list!

## New features

- Updated script
- Better code documentation
- Better command system:
  - Unwrap function
  - Encoding option

- Bug fixed:
        In some tests, the original tool placed the wrap tag
        between 3 and 4 times before the word,
        which takes up unnecessary space and makes the file heavier.
        Now the tool places only 1 tag per word!

## Credits

- **Edward Keyes**: Original tool creator
- **Digimaloko**: Code review
- **Yuno2k23**: The guy who modified and tested it in other games
