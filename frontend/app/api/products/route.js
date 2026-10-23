import { NextResponse } from 'next/server';

export async function GET() {
  try {
    const res = await fetch('http://127.0.0.1:8000/products', { cache: 'no-store' });

    const data = await res.json();
    if (!res.ok) {
      return NextResponse.json(data, { status: res.status });
    }

    return NextResponse.json(data);
  } catch (error) {
    console.error("Ошибка получения списка:", error);
    return NextResponse.json(
      { error: 'Не удалось получить список товаров' },
      { status: 502 }
    );
  }
}