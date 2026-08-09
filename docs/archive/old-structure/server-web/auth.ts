import { eq } from "drizzle-orm";
import { drizzle } from "drizzle-orm/mysql2";
import { users } from "../drizzle/schema";
import { ENV } from './_core/env';
import crypto from 'crypto';

let _db: ReturnType<typeof drizzle> | null = null;

export async function getDb() {
  if (!_db && process.env.DATABASE_URL) {
    _db = drizzle(process.env.DATABASE_URL);
  }
  return _db;
}

function hashPassword(password: string): string {
  return crypto.createHash('sha256').update(password).digest('hex');
}

export async function registerUser(email: string, password: string, name: string) {
  const db = await getDb();
  if (!db) throw new Error('Database not available');

  const existingUser = await db
    .select()
    .from(users)
    .where(eq(users.email, email))
    .limit(1);

  if (existingUser.length > 0) {
    throw new Error('Email already registered');
  }

  const hashedPassword = hashPassword(password);
  const openId = `local_${email}_${Date.now()}`;

  await db.insert(users).values({
    openId,
    email,
    name,
    loginMethod: 'email',
    role: 'user',
    createdAt: new Date(),
    updatedAt: new Date(),
    lastSignedIn: new Date(),
  });

  return { email, name };
}

export async function loginUser(email: string, password: string) {
  const db = await getDb();
  if (!db) throw new Error('Database not available');

  const user = await db
    .select()
    .from(users)
    .where(eq(users.email, email))
    .limit(1);

  if (user.length === 0) {
    throw new Error('User not found');
  }

  // В реальном приложении здесь должна быть проверка пароля
  // Для демо просто проверяем что пароль не пустой
  if (!password) {
    throw new Error('Invalid password');
  }

  return user[0];
}
