if __name__ == '__main__':
    from core.team import sql_generator_team
    import asyncio
    async def main():
        res = await sql_generator_team.generate_sql(
            "查询id为1的员工的所有信息包括部门")
        print('###########', res)
    asyncio.run(main())
