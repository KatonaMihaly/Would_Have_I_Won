MATCHES_HU7 = """
SELECT
    sub_a.draw_date,
    sub_a.numbers,
    sub_a.match_count AS match_count_a,
    sub_b.numbers,
    sub_b.match_count AS match_count_b,
    COUNT(*) OVER () AS total_count 
FROM
    (
        SELECT
            draw_date, numbers,
            CARDINALITY(ARRAY(
                SELECT UNNEST(numbers)
                INTERSECT
                SELECT UNNEST(:numbers_a) -- This is numbers_set_a
            )) AS match_count
        FROM draw
        WHERE lottery_id = :id_a -- This is lottery_id 'hu7a'
    ) AS sub_a

INNER JOIN
    (
        SELECT
            draw_date, numbers,
            CARDINALITY(ARRAY(
                SELECT UNNEST(numbers)
                INTERSECT
                SELECT UNNEST(:numbers_b) -- This is numbers_set_b
            )) AS match_count
        FROM draw
        WHERE lottery_id = :id_b -- This is lottery_id 'hu7b'
    ) AS sub_b
ON
    sub_a.draw_date = sub_b.draw_date
WHERE
    sub_b.match_count = :match_count OR
    sub_a.match_count = :match_count
ORDER BY
    sub_a.draw_date DESC
LIMIT 20;
"""

MATCHES_HU5_HU6 = """
SELECT *, COUNT(*) OVER () AS total_count 
FROM (
    SELECT draw_date, numbers,
           CARDINALITY(ARRAY(
               SELECT UNNEST(numbers)
               INTERSECT
               SELECT UNNEST(:number)
           )) AS match_count
    FROM draw
    WHERE lottery_id = :id
) AS sub
WHERE match_count = :match_count
ORDER BY draw_date DESC
LIMIT 20;
"""

MATCHES_TOTAL = "SELECT COUNT(*) FROM draw WHERE lottery_id = :id;"
