VIEWS_DICT = {
    "Q3":
        ["""CREATE VIEW Happy_Family AS
            Select hID
            From Households
            WHERE (size >= 3 AND netWorth > 5)
            ;""",
         """CREATE VIEW Reality_pcodes AS
            select pCode
            FROM Programs
            Where genre = 'Reality'
            ;""",
         """Create View reality_devices
            AS
            SELECT V.dID
            FROM Viewing V, Reality_pcodes R
            WHERE V.pCode = R.pCode
            ;""",

            """CREATE VIEW Reality_Families
            AS
            select D.hID
            From Devices D, reality_devices R
            Where D.dID = R.dID
            ;""",

            """CREATE VIEW Family_Devices
            AS
            SELECT H.hID, Count(D.hID) AS num_devices
            From Households H LEFT JOIN Devices D on H.hID = D.hID
            GROUP BY H.hID
            ;"""

        ]
    ,
    "Q4":
        [
         """CREATE VIEW Long_Shows AS
            SELECT P1.pCode ,P1.title, P1.genre, p1.duration
            FROM Programs P1
            Where P1.genre IS NOT NULL and P1.duration > ALL (SELECT P2.duration
                                                              FROM Programs P2
                                                              WHERE P1.genre = P2.genre and P1.pCode != P2.pCode)
            ;""",


            """CREATE View Popular_Shows AS
            SELECT X.pCode, X.title, x.Counter
            from (  SELECT LS.pCode, LS.title, COUNT(DISTINCT D.hID) as Counter
                    FROM Long_Shows LS INNER JOIN Viewing V on LS.pCode = V.pCode INNER JOIN Devices D on D.dID = V.dID
                    GROUP BY LS.pCode, LS.title) X
            Where X.Counter >= 3
            ;""",

            """CREATE View All_info AS
            SELECT PS.pCode, title, V.dID, eTime, hID
            FROM Popular_Shows PS INNER JOIN Viewing V on PS.pCode = V.pCode INNER JOIN Devices D on D.dID = V.dID
            ;""",


            """Create View Modern_families AS
            SELECT X.hID
            FROM (SELECT Ai.hID, COUNT(DISTINCT Ai.pCode) as num_shows
                  From All_info Ai INNER JOIN Popular_Shows PS on Ai.pCode = PS.pCode
                  GROUP BY Ai.hID) X
            WHERE X.num_shows >= 3
            ;"""
        ]
}