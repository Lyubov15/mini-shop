import { NextResponse } from 'next/server';

export async function GET(request, { params }) {
  const { id } = await params;
  const backendUrl = (process.env.BACKEND_URL || 'http://127.0.0.1:8000')
    .replace(/\/+$/, '');

  try {
    const res = await fetch(
      `${backendUrl}/products/${encodeURIComponent(id)}/image`,
      {
        headers: {
          'ngrok-skip-browser-warning': 'true',
        },
        cache: 'no-store',
      }
    );

    const contentType = res.headers.get('content-type');
    if (!res.ok || (contentType && !contentType.startsWith('image/'))) {
      return new NextResponse('Image not found', {
        status: res.ok ? 404 : res.status,
        headers: { 'Content-Type': 'text/plain; charset=utf-8' },
      });
    }

    if (!res.body) {
      return new NextResponse('Image response has no body', { status: 502 });
    }

    return new NextResponse(res.body, {
      headers: {
        'Content-Type': contentType || 'image/jpeg',
        'Content-Disposition': 'inline',
        'Cache-Control': 'public, max-age=86400',
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
