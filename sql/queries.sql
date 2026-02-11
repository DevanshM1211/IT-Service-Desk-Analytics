-- ============================================================================
-- IT SERVICE DESK ANALYTICS - SQL QUERIES
-- ============================================================================
-- Database: Service_Desk_Analytics
-- Table: service_tickets
-- Description: Analysis queries for IT Service Desk performance tracking
-- Author: Devansh Mehrotra
-- Last Updated: February 11, 2026
-- ============================================================================

-- TABLE STRUCTURE REFERENCE:
-- service_tickets (
--   Ticket_ID VARCHAR(20),
--   Created_Date DATETIME,
--   Resolved_Date DATETIME,
--   Priority VARCHAR(20),
--   Category VARCHAR(50),
--   Assigned_Team VARCHAR(50),
--   Resolution_Hours FLOAT,
--   SLA_Breached BOOLEAN,
--   SLA_Target_Hours INT,
--   Ticket_Age_Hours FLOAT
-- )

-- ============================================================================
-- QUERY 1: SLA COMPLIANCE PERCENTAGE
-- ============================================================================
-- Purpose: Calculate overall SLA compliance rate (tickets resolved within SLA)
-- Business Value: Executive KPI for service level performance
-- Output: Compliance percentage with compliant/total counts

SELECT 
    ROUND(
        (COUNT(CASE WHEN SLA_Breached = 0 THEN 1 END) * 100.0) / COUNT(*), 
        2
    ) AS SLA_Compliance_Percentage,
    COUNT(CASE WHEN SLA_Breached = 0 THEN 1 END) AS Compliant_Tickets,
    COUNT(CASE WHEN SLA_Breached = 1 THEN 1 END) AS Breached_Tickets,
    COUNT(*) AS Total_Tickets
FROM service_tickets;


-- ============================================================================
-- QUERY 2: AVERAGE RESOLUTION TIME BY CATEGORY
-- ============================================================================
-- Purpose: Identify which ticket categories take longest to resolve
-- Business Value: Resource allocation and process improvement insights
-- Output: Average resolution time sorted by longest resolution

SELECT 
    Category,
    ROUND(AVG(Resolution_Hours), 2) AS Avg_Resolution_Hours,
    ROUND(AVG(Resolution_Hours) / 24.0, 2) AS Avg_Resolution_Days,
    COUNT(*) AS Ticket_Count,
    MIN(Resolution_Hours) AS Min_Hours,
    MAX(Resolution_Hours) AS Max_Hours,
    ROUND(STDEV(Resolution_Hours), 2) AS StdDev_Hours
FROM service_tickets
GROUP BY Category
ORDER BY Avg_Resolution_Hours DESC;


-- ============================================================================
-- QUERY 3: TICKET VOLUME PER MONTH
-- ============================================================================
-- Purpose: Track ticket volume trends across months for capacity planning
-- Business Value: Identify seasonal patterns and forecasting
-- Output: Monthly ticket counts with growth rates

SELECT 
    FORMAT(Created_Date, 'yyyy-MM') AS Month,
    COUNT(*) AS Total_Tickets,
    COUNT(CASE WHEN Priority = 'Critical' THEN 1 END) AS Critical_Count,
    COUNT(CASE WHEN Priority = 'High' THEN 1 END) AS High_Count,
    COUNT(CASE WHEN Priority = 'Medium' THEN 1 END) AS Medium_Count,
    COUNT(CASE WHEN Priority = 'Low' THEN 1 END) AS Low_Count,
    ROUND(
        (COUNT(*) - LAG(COUNT(*)) OVER (ORDER BY FORMAT(Created_Date, 'yyyy-MM'))) * 100.0 / 
        LAG(COUNT(*)) OVER (ORDER BY FORMAT(Created_Date, 'yyyy-MM')),
        2
    ) AS Growth_Rate_Percent
FROM service_tickets
GROUP BY FORMAT(Created_Date, 'yyyy-MM')
ORDER BY Month;


-- ============================================================================
-- QUERY 4: TOP 5 RECURRING CATEGORIES
-- ============================================================================
-- Purpose: Identify most problematic ticket categories by frequency
-- Business Value: Priority areas for process improvement and training
-- Output: Top 5 categories with volume, percentage, breach rate

SELECT TOP 5
    Category,
    COUNT(*) AS Ticket_Count,
    ROUND((COUNT(*) * 100.0) / (SELECT COUNT(*) FROM service_tickets), 2) AS Percentage_of_Total,
    ROUND(
        (COUNT(CASE WHEN SLA_Breached = 1 THEN 1 END) * 100.0) / COUNT(*),
        2
    ) AS Breach_Rate_Percent,
    ROUND(AVG(Resolution_Hours), 2) AS Avg_Resolution_Hours,
    ROUND(AVG(Resolution_Hours) / 24.0, 2) AS Avg_Resolution_Days
FROM service_tickets
GROUP BY Category
ORDER BY Ticket_Count DESC;


-- ============================================================================
-- QUERY 5: BREACH COUNT BY ASSIGNED TEAM
-- ============================================================================
-- Purpose: Measure SLA breach performance by team for accountability
-- Business Value: Team performance evaluation and coaching insights
-- Output: Team breach statistics with compliance rates

SELECT 
    Assigned_Team,
    COUNT(*) AS Total_Tickets,
    COUNT(CASE WHEN SLA_Breached = 1 THEN 1 END) AS Breached_Tickets,
    COUNT(CASE WHEN SLA_Breached = 0 THEN 1 END) AS Compliant_Tickets,
    ROUND(
        (COUNT(CASE WHEN SLA_Breached = 1 THEN 1 END) * 100.0) / COUNT(*),
        2
    ) AS Breach_Rate_Percent,
    ROUND(
        (COUNT(CASE WHEN SLA_Breached = 0 THEN 1 END) * 100.0) / COUNT(*),
        2
    ) AS Compliance_Rate_Percent,
    ROUND(AVG(Resolution_Hours), 2) AS Avg_Resolution_Hours,
    ROUND(AVG(Resolution_Hours) / 24.0, 2) AS Avg_Resolution_Days
FROM service_tickets
GROUP BY Assigned_Team
ORDER BY Breach_Rate_Percent DESC;


-- ============================================================================
-- BONUS QUERY 1: SLA COMPLIANCE BY PRIORITY LEVEL
-- ============================================================================
-- Purpose: Analyze SLA performance variance by ticket priority
-- Business Value: Understand if higher-priority tickets receive better service
-- Output: Compliance metrics per priority level

SELECT 
    Priority,
    COUNT(*) AS Total_Tickets,
    COUNT(CASE WHEN SLA_Breached = 0 THEN 1 END) AS Compliant_Tickets,
    COUNT(CASE WHEN SLA_Breached = 1 THEN 1 END) AS Breached_Tickets,
    ROUND(
        (COUNT(CASE WHEN SLA_Breached = 0 THEN 1 END) * 100.0) / COUNT(*),
        2
    ) AS Compliance_Rate_Percent,
    ROUND(AVG(Resolution_Hours), 2) AS Avg_Resolution_Hours,
    ROUND(AVG(Resolution_Hours) / 24.0, 2) AS Avg_Resolution_Days
FROM service_tickets
GROUP BY Priority
ORDER BY 
    CASE 
        WHEN Priority = 'Critical' THEN 1
        WHEN Priority = 'High' THEN 2
        WHEN Priority = 'Medium' THEN 3
        WHEN Priority = 'Low' THEN 4
    END;


-- ============================================================================
-- BONUS QUERY 2: CATEGORY PERFORMANCE MATRIX
-- ============================================================================
-- Purpose: Comprehensive view of each category with all key metrics
-- Business Value: Single query for category health assessment
-- Output: Complete category benchmarking data

SELECT 
    Category,
    COUNT(*) AS Ticket_Count,
    ROUND(
        (COUNT(*) * 100.0) / (SELECT COUNT(*) FROM service_tickets),
        2
    ) AS Volume_Percent,
    ROUND(AVG(Resolution_Hours), 2) AS Avg_Hours,
    ROUND(AVG(Resolution_Hours) / 24.0, 2) AS Avg_Days,
    MIN(Resolution_Hours) AS Min_Hours,
    MAX(Resolution_Hours) AS Max_Hours,
    ROUND(STDEV(Resolution_Hours), 2) AS StdDev,
    COUNT(CASE WHEN SLA_Breached = 0 THEN 1 END) AS Compliant,
    COUNT(CASE WHEN SLA_Breached = 1 THEN 1 END) AS Breached,
    ROUND(
        (COUNT(CASE WHEN SLA_Breached = 1 THEN 1 END) * 100.0) / COUNT(*),
        2
    ) AS Breach_Percent
FROM service_tickets
GROUP BY Category
ORDER BY Ticket_Count DESC;


-- ============================================================================
-- BONUS QUERY 3: TEAM AND CATEGORY CROSS-TABULATION
-- ============================================================================
-- Purpose: Analyze which teams handle which categories most frequently
-- Business Value: Identify specialization patterns and workload distribution
-- Output: Team-Category matrix with ticket counts

SELECT 
    Assigned_Team AS Team,
    Category,
    COUNT(*) AS Ticket_Count,
    ROUND(AVG(Resolution_Hours), 2) AS Avg_Hours,
    ROUND(
        (COUNT(CASE WHEN SLA_Breached = 1 THEN 1 END) * 100.0) / COUNT(*),
        2
    ) AS Breach_Percent
FROM service_tickets
GROUP BY Assigned_Team, Category
ORDER BY Assigned_Team, Ticket_Count DESC;


-- ============================================================================
-- BONUS QUERY 4: OUTLIER DETECTION - LONG RESOLUTION TIMES
-- ============================================================================
-- Purpose: Identify tickets with unusually long resolution times (top 95th percentile)
-- Business Value: Root cause analysis opportunities and escalation patterns
-- Output: Tickets exceeding 95th percentile resolution time

DECLARE @PercentileThreshold FLOAT;
SET @PercentileThreshold = (
    SELECT PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY Resolution_Hours) 
    FROM service_tickets
);

SELECT 
    Ticket_ID,
    Created_Date,
    Resolved_Date,
    Priority,
    Category,
    Assigned_Team,
    Resolution_Hours,
    SLA_Target_Hours,
    SLA_Breached,
    ROUND(Resolution_Hours - @PercentileThreshold, 2) AS Hours_Above_95th_Percentile
FROM service_tickets
WHERE Resolution_Hours > @PercentileThreshold
ORDER BY Resolution_Hours DESC;


-- ============================================================================
-- BONUS QUERY 5: FIRST-CONTACT RESOLUTION EFFICIENCY
-- ============================================================================
-- Purpose: Identify fast-handled tickets (resolved < 24 hours)
-- Business Value: Best practice identification and efficiency benchmarking
-- Output: Quick-resolution metrics by team and category

SELECT 
    Category,
    Assigned_Team,
    COUNT(*) AS Total_Tickets,
    COUNT(CASE WHEN Resolution_Hours < 24 THEN 1 END) AS Quick_Resolution_Count,
    ROUND(
        (COUNT(CASE WHEN Resolution_Hours < 24 THEN 1 END) * 100.0) / COUNT(*),
        2
    ) AS Quick_Resolution_Percent,
    COUNT(CASE WHEN Resolution_Hours < 24 AND SLA_Breached = 0 THEN 1 END) AS Quick_And_Compliant,
    ROUND(AVG(CASE WHEN Resolution_Hours < 24 THEN Resolution_Hours ELSE NULL END), 2) AS Avg_Quick_Hours
FROM service_tickets
GROUP BY Category, Assigned_Team
HAVING COUNT(CASE WHEN Resolution_Hours < 24 THEN 1 END) > 0
ORDER BY Quick_Resolution_Percent DESC;


-- ============================================================================
-- SETUP & TESTING QUERIES
-- ============================================================================

-- View table structure
-- EXEC sp_help 'service_tickets';

-- Count total records
-- SELECT COUNT(*) AS TotalRecords FROM service_tickets;

-- Check data quality
-- SELECT 
--     COUNT(*) AS RecordCount,
--     COUNT(DISTINCT Ticket_ID) AS UniqueTickets,
--     COUNT(CASE WHEN Category IS NULL THEN 1 END) AS NullCategories,
--     MIN(Created_Date) AS EarliestTicket,
--     MAX(Created_Date) AS LatestTicket
-- FROM service_tickets;

-- ============================================================================
-- END OF QUERIES
-- ============================================================================
