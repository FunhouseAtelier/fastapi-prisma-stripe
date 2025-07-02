# app/utils/prisma.py

from prisma_client import Prisma, register

prisma = Prisma()


async def connect_prisma():
    await prisma.connect()
    register(prisma)  # Makes `from prisma import prisma` work globally


async def disconnect_prisma():
    await prisma.disconnect()
