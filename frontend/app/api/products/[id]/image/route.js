import { NextResponse } from 'next/server';

export async function GET(request, { params }) {
  const { id } = await params;

  try {
    const res = await fetch(`http://127.0.0.1:8000/products/${id}/image`, {
      cache: 'no-store',
    });

    if (!res.ok) {
      return new NextResponse(await res.text(), {
        status: res.status,
        headers: {
          'Content-Type': res.headers.get('Content-Type') || 'text/plain',
        },
      });
    }

    return new NextResponse(await res.arrayBuffer(), {
      headers: {
        'Content-Type': res.headers.get('Content-Type') || 'image/jpeg',
      },
    });
  } catch (error) {
    console.error(`Ошибка получения изображения товара ${id}:`, error);
    return NextResponse.json(
      { error: 'Не удалось получить изображение товара' },
      { status: 502 }
    );
  }
}
