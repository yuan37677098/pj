def is_leap_year(year):
    """
    判断给定年份是否为闰年
    
    规则：
    1. 能被4整除但不能被100整除
    2. 或者能被400整除
    
    参数:
        year: 年份（整数）
    
    返回:
        bool: 是闰年返回True，否则返回False
    """
    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
        return True
    return False


if __name__ == "__main__":
    test_years = [2000, 2004, 1900, 2024, 2023, 2100]
    for y in test_years:
        result = "是闰年" if is_leap_year(y) else "不是闰年"
        print(f"{y}年 {result}")
