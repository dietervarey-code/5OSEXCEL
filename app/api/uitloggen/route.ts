import { NextResponse } from 'next/server';
import { COOKIE_NAAM } from '@/lib/auth';

export async function POST() {
  const antwoord = NextResponse.json({ ok: true });
  antwoord.cookies.set(COOKIE_NAAM, '', { path: '/', maxAge: 0 });
  return antwoord;
}
