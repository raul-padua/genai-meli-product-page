"use client";

import Image from "next/image";
import { useEffect, useMemo, useState, useRef } from "react";
import styles from "./page.module.css";

const API_URL = process.env.NEXT_PUBLIC_API_URL || (typeof window !== 'undefined' ? '/py-api' : 'http://127.0.0.1:8000');

interface PaymentMethod {
  type: string;
  description: string;
}

interface SellerInfo {
  name: string;
  reputation: string;
  sales: number;
}

interface ItemDetail {
  id: string;
  title: string;
  description: string;
  price: number;
  currency: string;
  images: string[];
  payment_methods: PaymentMethod[];
  seller: SellerInfo;
  stock: number;
  ratings: number;
  reviews_count: number;
  heroImages: string[];
}

interface Review {
  id: string;
  rating: number;
  text: string;
  author: string;
  date: string;
  verified_purchase: boolean;
}

interface RatingBreakdown {
  five_stars: number;
  four_stars: number;
  three_stars: number;
  two_stars: number;
  one_star: number;
}

interface CharacteristicRating {
  name: string;
  rating: number;
}

interface ReviewsData {
  overall_rating: number;
  total_reviews: number;
  rating_breakdown: RatingBreakdown;
  characteristic_ratings: CharacteristicRating[];
  reviews: Review[];
}

interface SearchResult {
  title: string;
  url: string;
  content: string;
  score?: number;
}

const currencyFormatter = new Intl.NumberFormat("es-AR", {
  style: "currency",
  currency: "ARS",
  minimumFractionDigits: 0,
});

const RELATED_PRODUCTS = [
  {
    title: "Samsung Galaxy A55 5G Amarillo",
    price: 972000,
    image: "/galaxy_a55_amarillo.webp",
    badge: "Envío gratis",
  },
  {
    title: "Samsung Galaxy S24 256 GB Gris",
    price: 1450000,
    image: "/galaxy_s24_gris.webp",
    badge: "Envío gratis",
  },
  {
    title: "Samsung Galaxy A55 5G (Vista trasera)",
    price: 972000,
    image: "/hero_4.webp",
    badge: "Envío gratis",
  },
  {
    title: "Samsung Galaxy A55 5G (Detalle cámara)",
    price: 972000,
    image: "/hero_5.webp",
    badge: "Envío gratis",
  },
];

const ALSO_BOUGHT = [
  {
    title: "Samsung Galaxy A55 5G Azul",
    price: 972000,
    image: "/hero_1.webp",
  },
  {
    title: "Samsung Galaxy A55 5G Amarillo",
    price: 972000,
    image: "/galaxy_a55_amarillo.webp",
  },
  {
    title: "Samsung Galaxy S24 256 GB Gris",
    price: 1450000,
    image: "/galaxy_s24_gris.webp",
  },
  {
    title: "Tecno Spark 20 Pro+",
    price: 485000,
    image: "/tecno.webp",
  },
  {
    title: "Samsung Galaxy A55 5G (Vista lateral)",
    price: 972000,
    image: "/hero_3.webp",
  },
  {
    title: "Samsung Galaxy A55 5G (Vista trasera)",
    price: 972000,
    image: "/hero_4.webp",
  },
  {
    title: "Samsung Galaxy A55 5G (Detalle cámara)",
    price: 972000,
    image: "/hero_5.webp",
  },
];

const SPECIFICATIONS = [
  {
    label: "Memoria RAM",
    value: "8 GB",
  },
  {
    label: "Almacenamiento interno",
    value: "256 GB",
  },
  {
    label: "Cámara principal",
    value: "50 MP",
  },
  {
    label: "Cámara frontal",
    value: "32 MP",
  },
  {
    label: "Batería",
    value: "5000 mAh",
  },
  {
    label: "Procesador",
    value: "Exynos 1480 Octa-Core",
  },
  {
    label: "Pantalla",
    value: "6.6\" Super AMOLED 120 Hz",
  },
  {
    label: "Protección",
    value: "IP67 (agua y polvo)",
  },
];

export default function Home() {
  const [item, setItem] = useState<ItemDetail | null>(null);
  const [selectedImage, setSelectedImage] = useState<string>("");
  const [alsoBoughtIndex, setAlsoBoughtIndex] = useState<number>(0);
  const [sellerProductsIndex, setSellerProductsIndex] = useState<number>(0);
  const [reviews, setReviews] = useState<ReviewsData | null>(null);
  const [chatOpen, setChatOpen] = useState<boolean>(false);
  const [chatMessages, setChatMessages] = useState<{role: 'user'|'bot', text: string, timestamp: Date}[]>([]);
  const [chatInput, setChatInput] = useState<string>("");
  const [openaiKey, setOpenaiKey] = useState<string>("");
  const [isTyping, setIsTyping] = useState<boolean>(false);
  const chatBodyRef = useRef<HTMLDivElement>(null);
  
  // Search functionality
  const [searchQuery, setSearchQuery] = useState<string>("");
  const [searchResults, setSearchResults] = useState<SearchResult[]>([]);
  const [showSearchResults, setShowSearchResults] = useState<boolean>(false);
  const [isSearching, setIsSearching] = useState<boolean>(false);
  const searchTimeoutRef = useRef<NodeJS.Timeout | null>(null);

  const displayedImage = useMemo(() => {
    if (selectedImage) {
      return selectedImage;
    }
    return item?.images?.[0] || "";
  }, [selectedImage, item]);

  useEffect(() => {
    fetch(`${API_URL}/item`)
      .then((res) => res.json())
      .then((data: ItemDetail) => {
        setItem(data);
        // Set default selected image explicitly to ensure initial render shows the hero
        const firstImage = Array.isArray(data.images) && data.images.length > 0 ? data.images[0] : "";
        setSelectedImage(firstImage);
      })
      .catch((error) => {
        console.error("Failed to load item detail", error);
      });

    fetch(`${API_URL}/reviews`)
      .then((res) => res.json())
      .then((data) => {
        setReviews(data);
      })
      .catch((error) => {
        console.error("Failed to load reviews", error);
      });
  }, []);

  const cleanResponseText = (text: string): string => {
    return text
      // Remove markdown-style citations like [Opiniones destacadas]
      .replace(/\[([^\]]+)\]/g, '')
      // Remove asterisks used for emphasis
      .replace(/\*/g, '')
      // Remove angle brackets
      .replace(/[<>]/g, '')
      // Remove extra whitespace and clean up
      .replace(/\s+/g, ' ')
      .trim();
  };

  // Auto-scroll to bottom of chat
  useEffect(() => {
    if (chatBodyRef.current) {
      chatBodyRef.current.scrollTop = chatBodyRef.current.scrollHeight;
    }
  }, [chatMessages, isTyping]);

  // Search function with debouncing
  const performSearch = async (query: string) => {
    if (!query.trim()) {
      setSearchResults([]);
      setShowSearchResults(false);
      return;
    }

    setIsSearching(true);
    try {
      const response = await fetch(`${API_URL}/search`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query })
      });
      const data = await response.json();
      setSearchResults(data.results || []);
      setShowSearchResults(true);
    } catch (error) {
      console.error('Search error:', error);
      setSearchResults([]);
    } finally {
      setIsSearching(false);
    }
  };

  // Handle search input with debouncing
  const handleSearchInput = (value: string) => {
    setSearchQuery(value);
    
    // Clear existing timeout
    if (searchTimeoutRef.current) {
      clearTimeout(searchTimeoutRef.current);
    }
    
    // Set new timeout for debounced search
    searchTimeoutRef.current = setTimeout(() => {
      performSearch(value);
    }, 500); // 500ms debounce
  };

  // Handle search result click
  const handleSearchResultClick = (url: string) => {
    window.open(url, '_blank');
    setShowSearchResults(false);
    setSearchQuery("");
  };

  const sendChat = async () => {
    if (!chatInput.trim() || isTyping) return;
    const question = chatInput.trim();
    const now = new Date();
    setChatMessages((m) => [...m, { role: 'user', text: question, timestamp: now }]);
    setChatInput("");
    setIsTyping(true);
    
    try {
      const res = await fetch(`${API_URL}/agent/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question, openai_key: openaiKey || undefined })
      });
      const data = await res.json();
      const cleanedAnswer = cleanResponseText(data.answer);
      setChatMessages((m) => [...m, { role: 'bot', text: cleanedAnswer, timestamp: new Date() }]);
    } catch {
      setChatMessages((m) => [...m, { role: 'bot', text: 'Hubo un error consultando el asistente.', timestamp: new Date() }]);
    } finally {
      setIsTyping(false);
    }
  };

  const formattedPrice = useMemo(() => {
    if (!item) return "";
    return currencyFormatter.format(item.price);
  }, [item]);

  if (!item) {
    return <div>Loading...</div>;
  }

  return (
    <>
    <div className={styles.page}>
      <div className={styles.headerWrapper}>
        <header className={styles.banner}>
        <Image
          className={styles.logo}
            src="/logo_MELI.png"
            alt="Mercado Libre logo"
            width={200}
            height={56}
          priority
        />
          <div className={styles.searchBar}>
            <input 
              type="text" 
              placeholder="Buscar productos, marcas y más..." 
              value={searchQuery}
              onChange={(e) => handleSearchInput(e.target.value)}
              onFocus={() => searchResults.length > 0 && setShowSearchResults(true)}
              onBlur={() => setTimeout(() => setShowSearchResults(false), 200)}
            />
            <button type="button" onClick={() => performSearch(searchQuery)}>
              Buscar
            </button>
            {showSearchResults && (
              <div className={styles.searchDropdown}>
                {isSearching ? (
                  <div className={styles.searchLoading}>Buscando...</div>
                ) : searchResults.length > 0 ? (
                  searchResults.map((result, index) => (
                    <div 
                      key={index}
                      className={styles.searchResult}
                      onClick={() => handleSearchResultClick(result.url)}
                    >
                      <div className={styles.searchResultTitle}>{result.title}</div>
                      <div className={styles.searchResultContent}>{result.content}</div>
                      <div className={styles.searchResultUrl}>{result.url}</div>
                    </div>
                  ))
                ) : searchQuery.trim() && (
                  <div className={styles.searchNoResults}>No se encontraron resultados</div>
                )}
              </div>
            )}
          </div>
          <div className={styles.location}>
            <span>Enviar a:</span>
            <span>Capital Federal</span>
          </div>
        </header>
        <div className={styles.secondaryHeader}>
          <div className={styles.secondaryHeaderContent}>
            <span>Celulares y teléfonos &gt; Accesorios para celulares</span>
            <span>Compra protegida, recibí el producto que esperabas o te devolvemos tu dinero</span>
          </div>
        </div>
      </div>

      <main className={styles.main}>
        <div className={styles.mainInner}>
          <nav className={styles.breadcrumbs}>
            <span>Volver al listado</span>
            <span>&gt;</span>
            <span>Celulares y Teléfonos</span>
            <span>&gt;</span>
            <span>Samsung</span>
          </nav>

          <div className={styles.productShell}>
            <article className={styles.gallery}>
              <div className={styles.thumbnailList}>
                {item.images.map((img) => (
                  <button
                    key={img}
                    className={styles.thumbnail}
                    type="button"
                    onMouseEnter={() => {
                      console.log("Hovering over thumbnail:", img);
                      setSelectedImage(img);
                    }}
                    onFocus={() => setSelectedImage(img)}
                    onClick={() => {
                      console.log("Clicked thumbnail:", img);
                      setSelectedImage(img);
                    }}
                    aria-label="Seleccionar imagen"
                  >
                    <img src={img} alt="Miniatura del producto" />
                  </button>
                ))}
              </div>
              <div className={styles.mainImage}>
                <img 
                  src={displayedImage || "/hero_1.webp"} 
                  alt={item.title}
                  style={{maxWidth: '100%', maxHeight: '100%', objectFit: 'contain'}}
                  onLoad={() => console.log("Image loaded:", displayedImage || "/hero_1.webp")}
                  onError={() => {
                    console.error("Image failed to load:", displayedImage || "/hero_1.webp");
                    // Fallback to hero_1 if current image fails
                    if (displayedImage !== "/hero_1.webp") {
                      setSelectedImage("/hero_1.webp");
                    }
                  }}
                />
              </div>
              <div className={styles.productInfo}>
                <span className={styles.secondaryInfo}>Nuevo | {item.reviews_count.toLocaleString()} opiniones</span>
                <h1 className={styles.title}>{item.title}</h1>
                <div className={styles.ratingRow}>
                  <span className={styles.stars}>★★★★★</span>
                  <span>
                    {item.ratings} promedio | {item.reviews_count.toLocaleString()} calificaciones
                  </span>
                </div>
                <div className={styles.price}>{formattedPrice}</div>
                <span className={styles.installments}>
                  En 12x {currencyFormatter.format(item.price / 12)} sin interés
                </span>

                <div className={styles.colorSection}>
                  <h3>Color: <span className={styles.colorName}>Celeste</span></h3>
                  <div className={styles.colorOptions}>
                    <div className={styles.colorOption}>
                      <img src="/hero_2.webp" alt="Celeste" className={styles.colorImage} />
                    </div>
                  </div>
                </div>

                <div className={styles.productFeatures}>
                  <h3>Lo que tenés que saber de este producto</h3>
                  <ul className={styles.featuresList}>
                    <li>Memoria RAM: 8 GB.</li>
                    <li>Dispositivo desbloqueado para que elijas tu compañía telefónica preferida.</li>
                    <li>Memoria interna de 256 GB.</li>
                  </ul>
                  <a 
                    href="#specifications" 
                    className={styles.verCaracteristicas}
                    onClick={(e) => {
                      e.preventDefault();
                      document.getElementById('specifications')?.scrollIntoView({ behavior: 'smooth' });
                    }}
                  >
                    Ver características
                  </a>
                </div>

                <div className={styles.buyingOptions}>
                  <h3>Opciones de compra:</h3>
                  <p className={styles.newProductsLink}>
                    <span className={styles.linkText}>5 productos nuevos desde</span> <span className={styles.linkPrice}>$ 975.950</span>
                  </p>
                </div>
              </div>
              <div className={styles.purchaseActions}>
                <div className={styles.benefits}>
                  <span>Envío gratis a todo el país</span>
                  <span>Devolución gratis con Mercado Libre</span>
                  <span>{item.stock} unidades disponibles</span>
                </div>
                <div className={styles.buttons}>
                  <button className={styles.primaryButton} type="button">
                    Comprar ahora
                  </button>
                  <button className={styles.secondaryButton} type="button">
                    Agregar al carrito
                  </button>
                </div>

                <div className={styles.sellerInfo}>
                  <div className={styles.sellerHeader}>
                    <div>
                      <p className={styles.sellerName}>{item.seller.name}</p>
                      <p>MercadoLíder {item.seller.reputation}</p>
                    </div>
                    <div className={styles.reputation}>
                      <div className={styles.officialStoreBadge}>Tienda oficial</div>
                      <span>{item.seller.sales.toLocaleString("es-AR")} ventas</span>
                    </div>
                  </div>
                  <ul className={styles.list}>
                    <li>Atención personalizada</li>
                    <li>Garantía oficial de 12 meses</li>
                    <li>Facturación electrónica disponible</li>
                  </ul>
                </div>

              </div>

              <div className={styles.paymentMethodsBoxSeparate}>
                <h3 className={styles.sectionTitle}>Medios de pago</h3>
                <div className={styles.paymentSection}>
                  <div className={styles.paymentCategory}>
                    <h4>Cuotas sin Tarjeta</h4>
                    <div className={styles.paymentLogos}>
                      <img src="/cuotas_sin_tarjeta_logo.png" alt="Mercado Pago" className={styles.paymentLogo} />
                    </div>
                  </div>
                  
                  <div className={styles.paymentCategory}>
                    <h4>Tarjetas de crédito</h4>
                    <div className={styles.paymentLogos}>
                      <img src="/tarjetas_debido_logos.png" alt="Tarjetas de crédito" className={styles.paymentLogo} />
                    </div>
                  </div>

                  <div className={styles.paymentCategory}>
                    <h4>Tarjetas de débito</h4>
                    <div className={styles.paymentLogos}>
                      <img src="/tarjetas_debido_logos.png" alt="Tarjetas de débito" className={styles.paymentLogo} />
                    </div>
                  </div>

                  <div className={styles.paymentCategory}>
                    <h4>Efectivo</h4>
                    <div className={styles.paymentLogos}>
                      <img src="/efectivo_logos.png" alt="Efectivo" className={styles.paymentLogo} />
                    </div>
                  </div>

                  <a href="#" className={styles.morePaymentMethods}>Conocé otros medios de pago</a>
                </div>
              </div>

              <div className={styles.relatedProductsBoxSeparate}>
                <h3 className={styles.sectionTitle}>Productos relacionados</h3>
                <div className={styles.relatedProductsList}>
                  {RELATED_PRODUCTS.map((product, index) => (
                    <div className={styles.relatedProductItem} key={product.title}>
                      <img src={product.image} alt={product.title} />
                      <div className={styles.relatedProductInfo}>
                        <span className={styles.relatedProductTitle}>{product.title}</span>
                        <span className={styles.relatedProductPrice}>
                          {currencyFormatter.format(product.price)}
                        </span>
                        {product.badge && (
                          <span className={styles.relatedProductBadge}>{product.badge}</span>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            <section className={styles.upperLeftSections}>
              <div className={styles.leftSectionItem}>
                <div className={styles.carouselHeader}>
                  <h2 className={styles.sectionTitle}>Quienes vieron este producto también compraron</h2>
                </div>
                <div className={styles.carouselContainer}>
                  <button 
                    type="button" 
                    onClick={() => setAlsoBoughtIndex(Math.max(0, alsoBoughtIndex - 1))}
                    disabled={alsoBoughtIndex === 0}
                    className={styles.carouselButton}
                  >
                    ‹
                  </button>
                  <div className={styles.carouselTrack}>
                  {ALSO_BOUGHT.slice(alsoBoughtIndex, alsoBoughtIndex + 3).map((product) => (
                    <div className={styles.carouselItem} key={product.title}>
                      <img src={product.image} alt={product.title} />
                      <div>
                        <span>{product.title}</span>
                        <span className={styles.relatedPrice}>
                          {currencyFormatter.format(product.price)}
                        </span>
                      </div>
                    </div>
                  ))}
                  </div>
                  <button 
                    type="button" 
                    onClick={() => setAlsoBoughtIndex(Math.min(ALSO_BOUGHT.length - 3, alsoBoughtIndex + 1))}
                    disabled={alsoBoughtIndex >= ALSO_BOUGHT.length - 3}
                    className={styles.carouselButton}
                  >
                    ›
                  </button>
                </div>
              </div>



              <div className={styles.leftSectionItem}>
                <div className={styles.carouselHeader}>
                  <h2 className={styles.sectionTitle}>Productos del vendedor</h2>
                </div>
                <div className={styles.carouselContainer}>
                  <button 
                    type="button" 
                    onClick={() => setSellerProductsIndex(Math.max(0, sellerProductsIndex - 1))}
                    disabled={sellerProductsIndex === 0}
                    className={styles.sellerCarouselButton}
                  >
                    ‹
                  </button>
                  <div className={styles.carouselTrack}>
                    {RELATED_PRODUCTS.slice(sellerProductsIndex, sellerProductsIndex + 2).map((product) => (
                      <div className={`${styles.carouselItem} ${styles.sellerCarouselItem}`} key={product.title}>
                        <img src={product.image} alt={product.title} />
                        <div>
                          <span>{product.title}</span>
                          <span className={styles.relatedPrice}>
                            {currencyFormatter.format(product.price)}
                          </span>
                        </div>
                      </div>
                    ))}
                  </div>
                  <button 
                    type="button" 
                    onClick={() => setSellerProductsIndex(Math.min(RELATED_PRODUCTS.length - 2, sellerProductsIndex + 1))}
                    disabled={sellerProductsIndex >= RELATED_PRODUCTS.length - 2}
                    className={styles.sellerCarouselButton}
                  >
                    ›
                  </button>
                </div>
              </div>
            </section>

            <section className={styles.lowerLeftSections}>
              <div className={styles.leftSectionItem} id="specifications">
              <h2 className={styles.sectionTitle}>Características del producto</h2>
              
              <div className={styles.screenSizeGraphic}>
                <div className={styles.screenSizeIcon}>
                  <div className={styles.screenIcon}>📱</div>
                </div>
                <div className={styles.screenSizeInfo}>
                  <div className={styles.screenSizeText}>
                    Tamaño de la pantalla: <strong>6.6&quot;</strong>
                  </div>
                  <div className={styles.screenSizeDimensions}>
                    (16.11 cm x 7.74 cm x 8.2 mm)
                  </div>
                  <div className={styles.screenSizeBar}>
                    <div className={styles.barSegments}>
                      <div className={styles.barSegment}></div>
                      <div className={styles.barSegment}></div>
                      <div className={styles.barSegment}></div>
                      <div className={styles.barSegment}></div>
                      <div className={styles.barSegmentActive}></div>
                    </div>
                    <div className={styles.barLabels}>
                      <span className={styles.barLabelSmall}>PEQUEÑO</span>
                      <span className={styles.barLabelLarge}>GRANDE</span>
                    </div>
                  </div>
                </div>
              </div>
                <div className={styles.specGrid}>
                  {SPECIFICATIONS.map((spec) => (
                    <div className={styles.specItem} key={spec.label}>
                      <span className={styles.highlight}>{spec.label}</span>
                      <span>{spec.value}</span>
                    </div>
                  ))}
                </div>
              </div>

              <div className={styles.leftSectionItem}>
              <h2 className={styles.sectionTitle}>Descripción</h2>
              <p>{item.description}</p>
              <p className={styles.highlight}>Capacidad y eficiencia</p>
              <p>
                Con un procesador Exynos 1480 y 8 GB de RAM vas a tener un rendimiento excepcional para aplicaciones, juegos y
                multitarea en Android 14 One UI 6.1.
              </p>
                <p className={styles.highlight}>Experiencia multimedia inmersiva</p>
              <p>
                La pantalla Super AMOLED de 6.6&quot; ofrece colores vivos y contraste intenso con Vision Booster, ideal para ver
                contenido en exteriores, mientras que Dolby Atmos brinda sonido envolvente.
              </p>
              <p className={styles.highlight}>Seguridad y autonomía</p>
              <p>
                Incluye lector de huellas en pantalla, Samsung Knox Vault y batería de 5000 mAh con carga rápida de 25 W para que
                te acompañe todo el día.
              </p>
              </div>

              {reviews && (
                <div className={styles.leftSectionItem}>
                  <h2 className={styles.sectionTitle}>Opiniones del producto</h2>
                  
                  <div className={styles.reviewsContainer}>
                    <div className={styles.reviewsLeft}>
                      <div className={styles.overallRating}>
                        <div className={styles.ratingNumber}>{reviews.overall_rating}</div>
                        <div className={styles.starsContainer}>
                          {[...Array(5)].map((_, i) => (
                            <span key={i} className={styles.star}>★</span>
                          ))}
                        </div>
                        <div className={styles.totalReviews}>{reviews.total_reviews} calificaciones</div>
                      </div>


                      <div className={styles.characteristicRatings}>
                        <h3 className={styles.characteristicTitle}>Calificación de características</h3>
                        {reviews.characteristic_ratings.map((char: CharacteristicRating, index: number) => (
                          <div key={index} className={styles.characteristicItem}>
                            <span className={styles.characteristicName}>{char.name}</span>
                            <div className={styles.characteristicStars}>
                              {[...Array(5)].map((_, i) => {
                                const isFullyFilled = i < Math.floor(char.rating);
                                const isHalfFilled = i === Math.floor(char.rating) && char.rating % 1 !== 0;
                                
                                return (
                                  <span 
                                    key={i} 
                                    className={`${styles.characteristicStar} ${
                                      isFullyFilled 
                                        ? styles.filled 
                                        : isHalfFilled 
                                          ? styles.halfFilled 
                                          : styles.empty
                                    }`}
                                  >
                                    ★
                                  </span>
                                );
                              })}
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>

                    <div className={styles.reviewsRight}>
                      <div className={styles.photoReviews}>
                        <h3 className={styles.photoReviewsTitle}>Opiniones con fotos</h3>
                        <div className={styles.photoThumbnails}>
                          {[1, 2, 3, 4].map((photoNum) => (
                            <div key={photoNum} className={styles.photoThumbnail}>
                              <img src={`/opinion_photo_${photoNum}.webp`} alt={`Review photo ${photoNum}`} />
                              <div className={styles.photoRating}>5 ★</div>
                            </div>
                          ))}
                        </div>
                        <div className={styles.reviewFilters}>
                          <div className={styles.filterButton}>Ordenar</div>
                          <div className={styles.filterButton}>Calificación</div>
                        </div>
                        <div className={styles.verifiedBadge}>
                          <span className={styles.checkmark}>✓</span>
                          Comprado a Tienda oficial Samsung
                        </div>
                      </div>

                      <div className={styles.highlightedReviews}>
                        <h3 className={styles.highlightedTitle}>Opiniones destacadas</h3>
                        <div className={styles.commentCount}>122 comentarios</div>
                        <div className={styles.reviewsList}>
                          {reviews.reviews.map((review: Review) => (
                            <div key={review.id} className={styles.reviewItem}>
                              <div className={styles.reviewHeader}>
                                <div className={styles.reviewStars}>
                                  {[...Array(5)].map((_, i) => (
                                    <span key={i} className={styles.reviewStar}>★</span>
                                  ))}
                                </div>
                                <div className={styles.reviewMeta}>
                                  <span className={styles.reviewAuthor}>{review.author}</span>
                                  <span className={styles.reviewDate}>{review.date}</span>
                                </div>
                              </div>
                              <p className={styles.reviewText}>{review.text}</p>
                            </div>
                          ))}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </section>
            </article>
          </div>
        </div>
      </main>
    </div>

    {/* Floating chat widget */}
    <button className={styles.chatFab} onClick={() => setChatOpen((v) => !v)} aria-label="Abrir asistente">
      {chatOpen ? '×' : '?'}
    </button>
    {chatOpen && (
      <div className={styles.chatPanel}>
        <div className={styles.chatHeader}>Asistente de producto</div>
        <div className={styles.apiKeyRow}>
          <input 
            type="password"
            value={openaiKey} 
            onChange={(e) => setOpenaiKey(e.target.value)} 
            placeholder="OpenAI API Key (opcional)" 
            className={styles.apiKeyInput}
          />
        </div>
        <div className={styles.chatBody} ref={chatBodyRef}>
          {chatMessages.map((m, idx) => (
            <div key={idx} className={m.role === 'user' ? styles.chatBubbleUser : styles.chatBubbleBot}>
              <div className={styles.messageText}>{m.text}</div>
              <div className={styles.messageTimestamp}>
                {m.timestamp.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' })}
              </div>
            </div>
          ))}
          {isTyping && (
            <div className={styles.chatBubbleBot}>
              <div className={styles.typingIndicator}>
                <span>Escribiendo</span>
                <div className={styles.typingDots}>
                  <span>.</span>
                  <span>.</span>
                  <span>.</span>
                </div>
              </div>
            </div>
          )}
          {chatMessages.length === 0 && !isTyping && (
            <div className={styles.chatBubbleBot}>
              Hola, ¿en qué te ayudo? Podés preguntar por características, cámaras, batería o cuotas.
              {!openaiKey && <><br/><br/><strong>💡 Tip:</strong> Ingresá tu OpenAI API Key arriba para respuestas más inteligentes con GPT-4.</>}
            </div>
          )}
        </div>
        <div className={styles.chatInputRow}>
          <input 
            value={chatInput} 
            onChange={(e) => setChatInput(e.target.value)} 
            placeholder="Escribe tu pregunta..." 
            onKeyDown={(e) => { if (e.key === 'Enter' && !isTyping) sendChat(); }} 
            disabled={isTyping}
          />
          <button onClick={sendChat} disabled={isTyping || !chatInput.trim()}>
            {isTyping ? 'Enviando...' : 'Enviar'}
          </button>
        </div>
    </div>
    )}
    </>
  );
}
