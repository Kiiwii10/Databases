QUERY_ANSWERS = {
    "Q3":
        """
        SELECT FD.hID, FD.num_devices
        From (SELECT hID FROM Happy_Family EXCEPT SELECT hID FROM Reality_Families) Class
            ,Family_Devices FD
        WHERE FD.hID = Class.hID
        """
    ,
    "Q4":
        """
        SELECT X.hID, X.title, Y.eTime
        FROM (  SELECT MF.hID, MIN (ai.eTime) as eTime
                FROM Modern_families MF INNER JOIN All_info Ai on MF.hID = Ai.hID
                GROUP BY MF.hID) Y
                INNER JOIN All_info X ON Y.hID = X.hID and Y.eTime = X.eTime
        ORDER BY Y.eTime, X.hID
        """
}
