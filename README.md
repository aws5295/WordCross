# WordCross Solver
I play a mobile game called [Wordscapes](https://play.google.com/store/apps/details?id=com.peoplefun.wordcross&hl=en_US), in which you are given 5-8 letters, and need to fill in a grid of words that can be spelled using those words.

![Wordscapes](https://lh3.googleusercontent.com/9x7r6ZPTGwxD8JhL0fRfhDv-2XQQqUoPGNsFs3qsMGEp0jQ59DSfPm-3-1hpfgVN5g=w1920-h1089-rw)

After being stuck for an embarassing amount of time on a level, I decided to make a solver in Python that prompts the user for their starting leters, and then shows them every possible word that can be made from those letters.

## Brute Force
My first crack at this problem was a simple brute force algorithm:
- (Pre-processing) Split a master list of every word into 26 separate files based on starting letter
- For each letter in my given letters:
  - Open the file for words starting with that letter
  - Loop through each word and see if it can be composed with only the given letters
  
This solution of course worked fine, but I wanted to do something more interesting/efficient.

## Tree Solution
My second solution involves performing further preprocessing of the data in order to process the possible words faster:
- (Pre-processing) Split a master list of every word into 26 separate files based on starting letter
- (Pre-processing) Process each file into a word tree (see [here](https://github.com/aws5295/WordCross/blob/master/DataFiles/readme.txt) for description) which gets serialized to a file
- For each letter in my given letters:
  - Deserialize the tree rooted with that letter
  - Crawl the tree, only visiting child branches if we have those letters available to us in our given letters
  - Any crawled nodes that are Words get added to the results list

The solution is more efficicent than the **brute force** solution because every child branch we visit is guaranteed to be leading us towards a valid word, so we are not wasting evaluations on paths that spell words that we can't form using our given letters.

## Sample Run
Input:
```
Enter a letter (Press <ENTER> to stop): b
Current Letters: B
Enter a letter (Press <ENTER> to stop): a
Current Letters: B A
Enter a letter (Press <ENTER> to stop): l
Current Letters: B A L
Enter a letter (Press <ENTER> to stop): e
Current Letters: B A L E
Enter a letter (Press <ENTER> to stop): l
Current Letters: B A L E L
Enter a letter (Press <ENTER> to stop):
Computing possible word compinations...
```

Output:
```
2-Letter Words:
BE
3-Letter Words:
ABE
ALB
ALE
ALL
BEL
ELL
LAB
LEA
4-Letter Words:
ABEL
ABLE
BALE
BALL
BELL
ELAL
5-Letter Words:
LABEL
```
