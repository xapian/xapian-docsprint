Verifying the index using xapian-delve
--------------------------------------

Xapian comes with a handy utility called `xapian-delve` which can be used to
inspect a database, so let's look at the one you just built. If you just
pass a database path as a parameter you'll get an overview: how many documents,
average term length, and some other statistics:

.. code-block:: none

    $ xapian-delve db
    UUID = 1820ef0a-055b-4946-ae73-67aa4ef5c226
    number of documents = 100
    average document length = 186.04
    document length lower bound = 8
    document length upper bound = 712
    highest document id ever used = 102
    has positional information = true
    currently open for writing = false

You can also look at an individual document, using Xapian's docid (``-d``
means output document data as well):

.. code-block:: none

    $ xapian-delve -r 1 -d db       # output has been reformatted
    Data for record #1:
    {
       "id_NUMBER" : "1896-16-14",
       "DATE_MADE" : "1660–70",
       "MATERIALS" : "black;red;crayon;brush;white;heightening;bluegrey;paper",
       "NAME_unused" : "",
       "WHOLE_PART_unused" : "",
       "TITLE" : "Study of a nude elderly man, Bacchus or one of his companions",
       "MEASUREMENTS" : "428 x 668 mm",
       "DESCRIPTION" : "Figure crowned with vine leaves is shown sitting upon stone which is covered by cloth. Lower part of body and head are shown in profile, whereas chest is turned toward front, the left arm crossing right leg. Raised right hand is leaned upon staff.",
       "COLLECTION" : "Cooper Hewitt, Smithsonian Design Museum",
       "PLACE_MADE_unused" : "",
       "MAKER" : "Giovanni Battista Merano"
    }
    Term List for record #1: Q1896-16-14 Sa Sbacchus Scompanions
    Selderly Shis Sman Snude Sof Sone Sor Sstudy XDand XDare XDarm
    XDbody XDby XDchest XDcloth XDcovered XDcrossing XDcrowned
    XDfigure XDfront XDhand XDhead XDin XDis XDleaned XDleaves XDleft
    XDleg XDlower XDof XDpart XDprofile XDraised XDright XDshown
    XDsitting XDstaff XDstone XDthe XDtoward XDturned XDupon XDvine
    XDwhereas XDwhich XDwith ZSa ZSbacchus ZScompanion ZSelder ZShis
    ZSman ZSnude ZSof ZSone ZSor ZSstudi ZXDand ZXDare ZXDarm ZXDbodi
    ZXDby ZXDchest ZXDcloth ZXDcover ZXDcross ZXDcrown ZXDfigur
    ZXDfront ZXDhand ZXDhead ZXDin ZXDis ZXDlean ZXDleav ZXDleft
    ZXDleg ZXDlower ZXDof ZXDpart ZXDprofil ZXDrais ZXDright ZXDshown
    ZXDsit ZXDstaff ZXDstone ZXDthe ZXDtoward ZXDturn ZXDupon ZXDvine
    ZXDwherea ZXDwhich ZXDwith Za Zand Zare Zarm Zbacchus Zbodi Zby
    Zchest Zcloth Zcompanion Zcover Zcross Zcrown Zelder Zfigur Zfront
    Zhand Zhead Zhis Zin Zis Zlean Zleav Zleft Zleg Zlower Zman Znude
    Zof Zone Zor Zpart Zprofil Zrais Zright Zshown Zsit Zstaff Zstone
    Zstudi Zthe Ztoward Zturn Zupon Zvine Zwherea Zwhich Zwith a and
    are arm bacchus body by chest cloth companions covered crossing
    crowned elderly figure front hand head his in is leaned leaves
    left leg lower man nude of one or part profile raised right shown
    sitting staff stone study the toward turned upon vine whereas
    which with

You can also go the other way, starting with a term and finding both
statistics and which documents it indexes:

.. code-block:: none

    $ xapian-delve -t Stime db
    Posting List for term 'Stime' (termfreq 1, collfreq 1, wdf_max 1): 81

This means you can look documents up by identifier:

.. code-block:: none

    $ xapian-delve -t Q1896-16-14 db
    Posting List for term 'Q1896-16-14' (termfreq 1, collfreq 0, wdf_max 0): 1

``xapian-delve`` is frequently useful if you aren't getting the behaviour you
expect from a search system, to check that the database contains the
documents and terms you expect.
