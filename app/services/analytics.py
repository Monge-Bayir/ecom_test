import asyncpg


async def more_than_3_twos(pool: asyncpg.Pool):
    sql = """
    SELECT full_name, COUNT(*)::int AS count_twos
    FROM grades
    WHERE grade = 2
    GROUP BY full_name
    HAVING COUNT(*) > 3
    ORDER BY count_twos DESC, full_name;
    """
    return await pool.fetch(sql)


async def less_than_5_twos(pool: asyncpg.Pool):
    sql = """
    SELECT full_name, COUNT(*)::int AS count_twos
    FROM grades
    WHERE grade = 2
    GROUP BY full_name
    HAVING COUNT(*) < 5
    ORDER BY count_twos ASC, full_name;
    """
    return await pool.fetch(sql)