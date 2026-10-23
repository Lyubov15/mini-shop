import { NextResponse } from 'next/server';

export async function DELETE(request, { params }) {
  const { id } = await params;
  try {
    const res = await fetch(`http://127.0.0.1:8000/products/${id}`, {
      method: 'DELETE',
      cache: 'no-store',
    });

    const body = await res.text();
    return new NextResponse(body, {
      status: res.status,
      headers: {
        'Content-Type': res.headers.get('Content-Type') || 'application/json',
      },
    });
  } catch (error) {
    console.error(`Ошибка удаления товара ${id}:`, error);
    return NextResponse.json(
      { error: 'Не удалось удалить товар' },
      { status: 502 }
    );
  }
}