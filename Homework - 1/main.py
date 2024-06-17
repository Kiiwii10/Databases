QUERIES_ANSWER = {
    "Q2":
        """
        select r.compID, r.depName, count(DISTINCT eID) as Employees_Count
        from (  select c.compID, c.depName, c.eID, c.pID
                from (  Select COUNT(wDate) as months_count, compID, depName, pID, eID
                        From WorkOnProject
                        GROUP BY compID, depName, pID, eID) c
                where months_count >= 6) r
        group by r.compID, r.depName
        """
    ,
    "Q3":
        """
        select comp.compID, comp.Avg_Budget
        from (  select DISTINCT p.compID, avg(p.budget) as Avg_Budget
                from Project p
                group by p.compID) as comp
        where comp.compID not in(   select companies.compID
                                    from (  select wages.compID, wages.depName, wages.pID, wages.budget, sum(Monthly_wage) as wage
                                            from (  select p.compID, p.depName, p.pID, p.budget, w.wDate, w.eID, (w.hours * e.hourlyWage) as Monthly_wage
                                                    from ((project p inner join WorkOnProject w
                                                    ON p.compID = w.compID and p.depName = w.depName and p.pID = w.pID)
                                                    inner join Employee e ON w.eID = e.eID)) wages
                                            GROUP BY wages.compID, wages.depName, wages.pID, wages.budget) as companies
                                    where budget < wage
                                    group by companies.compID)
        group by comp.compID, comp.Avg_Budget
        order by Avg_Budget DESC
        """
    ,
    "Q4":
        """
        select distinct proj_dep.compID
        from            (select compID, depName, count(pID) as num_projects
                        from Project
                        group by compID, depName) proj_dep
            inner join (select DISTINCT w.compID, w.depName, w.eID, e.hourlyWage, count(w.pID) as num_projects
                        from WorkOnProject w inner join Employee e
                        On w.eID = e.eID
                        group by w.compID, w.depName, w.eID, e.hourlyWage) proj_emp
            ON proj_dep.num_projects = proj_emp.num_projects
            inner join (select compID, depName, MAX(hourlyWage) as max_depart_wage
                        from Employee
                        group by compID, depName) as dep_max_wages
            ON dep_max_wages.max_depart_wage = hourlyWage
        group by proj_dep.compID
        """
}

