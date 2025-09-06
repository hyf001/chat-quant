
import pymysql
from . import config
import logging


mysql_config = config.config.get("mysql")
logger = logging.getLogger("execute_sql")

def execute_sql(sql):
    conn = None
    cursor = None
    try:
        conn = pymysql.connect(**mysql_config)
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def execute_sql(sql,*args):
    conn = None
    cursor = None
    try:
        conn = pymysql.connect(**mysql_config)
        cursor = conn.cursor()
        cursor.execute(sql,args=args)
        conn.commit
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def execute_batch(sql,args: list[tuple]):
    conn = None
    cursor = None
    try:
        logger.info(f"批量执行sql={sql}")
        conn = pymysql.connect(**mysql_config)
        cursor = conn.cursor()
        for arg in args:
            cursor.execute(sql,arg)
        conn.commit
       
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
