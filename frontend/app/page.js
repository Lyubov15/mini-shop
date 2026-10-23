"use client";

import { useEffect, useState } from "react";

export default function Home() {
  const [products, setProducts] = useState([]);

  useEffect(() => {
    fetch("/api/products")
      .then((res) => {
        if (!res.ok) {
          throw new Error(`Ошибка загрузки товаров: HTTP ${res.status}`);
        }
        return res.json();
      })
      .then((data) => setProducts(data))
      .catch((err) => console.error("Ошибка загрузки:", err));
  }, []);

  const handleDelete = async (id) => {
    if (!window.confirm("Удалить этот товар?")) return;
    
    try {
      const res = await fetch(`/api/products/${id}`, { method: "DELETE" });
      if (res.ok) {
        setProducts(products.filter((p) => p.id !== id));
      } else {
        alert("Ошибка при удалении");
      }
    } catch (err) {
      console.error(err);
      alert("Ошибка сети");
    }
  };

  return (
    <main style={{ padding: "20px", fontFamily: "sans-serif" }}>
      <h1 style={{ textAlign: "center" }}>Каталог</h1>

      {products.length === 0 ? (
        <p style={{ textAlign: "center" }}>Товаров пока нет. Добавь их через бота</p>
      ) : (
        <div style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fill, minmax(250px, 1fr))",
          gap: "20px"
        }}>
          {products.map((product) => (
            <div key={product.id} style={{
              border: "1px solid #ddd",
              borderRadius: "8px",
              padding: "15px",
              boxShadow: "0 2px 5px rgba(0,0,0,0.1)"
            }}>
              <img
                src={`/api/products/${product.id}/image`}
                alt={product.name}
                style={{ width: "100%", height: "200px", objectFit: "cover", borderRadius: "4px" }}
              />
              
              <h3 style={{ marginTop: "10px" }}>{product.name}</h3>
              
              <button 
                onClick={() => handleDelete(product.id)}
                style={{
                  marginTop: "10px",
                  width: "100%",
                  padding: "8px",
                  background: "#ff4d4f",
                  color: "white",
                  border: "none",
                  borderRadius: "4px",
                  cursor: "pointer"
                }}
              >
                Удалить
              </button>
            </div>
          ))}
        </div>
      )}
    </main>
  );
}