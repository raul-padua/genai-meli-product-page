"use client";

import Image from "next/image";
import { useEffect, useMemo, useState, useRef } from "react";
import styles from "./page.module.css";

const API_URL = process.env.NEXT_PUBLIC_API_URL || (typeof window !== 'undefined' ? '/py-api' : 'http://127.0.0.1:8000');

type Language = 'es' | 'pt' | 'en';

const translations = {
  es: {
    loading: "Cargando...",
    searchPlaceholder: "Buscar productos, marcas y más...",
    searchButton: "Buscar",
    searching: "Buscando...",
    noResults: "No se encontraron resultados",
    sendTo: "Enviar a:",
    city: "Capital Federal",
    breadcrumb1: "Celulares y teléfonos",
    breadcrumb2: "Accesorios para celulares",
    protectedPurchase: "Compra protegida, recibí el producto que esperabas o te devolvemos tu dinero",
    backToList: "Volver al listado",
    breadcrumbCategory: "Celulares y Teléfonos",
    newProduct: "Nuevo",
    soldCount: "vendidos",
    stock: "Stock disponible:",
    units: "unidades",
    quantity: "Cantidad:",
    color: "Color:",
    blue: "Azul",
    buyNow: "Comprar ahora",
    addToCart: "Agregar al carrito",
    freeShipping: "Envío gratis",
    arriving: "Llega",
    tomorrow: "mañana",
    seeShippingCosts: "Ver cómo llega",
    soldBy: "Vendido por",
    reputation: "Reputación",
    sales: "ventas",
    returns: "Devolución gratis",
    returnsDesc: "Tenés 30 días desde que lo recibís.",
    warranty: "Garantía",
    warrantyDesc: "Compra Protegida con Mercado Pago.",
    securePayment: "Pago seguro",
    securePaymentDesc: "Recibí el producto que esperabas o te devolvemos tu dinero.",
    paymentMethods: "Medios de pago",
    creditCards: "Tarjetas de crédito",
    debitCards: "Tarjetas de débito",
    cash: "Efectivo",
    installmentsTitle: "Cuotas sin tarjeta",
    installmentsDesc: "Comprá en cuotas sin tarjeta con Mercado Crédito.",
    knowMore: "Conocer más",
    description: "Descripción",
    specifications: "Características técnicas",
    specRAM: "Memoria RAM",
    specStorage: "Almacenamiento interno",
    specMainCamera: "Cámara principal",
    specFrontCamera: "Cámara frontal",
    specBattery: "Batería",
    specProcessor: "Procesador",
    specScreen: "Pantalla",
    specProtection: "Protección",
    reviewsTitle: "Opiniones del producto",
    overallRating: "Calificación general",
    reviews: "opiniones",
    stars: "estrellas",
    reviewBreakdown: "Desglose de calificaciones",
    characteristics: "Características destacadas",
    verifiedPurchase: "Compra verificada",
    alsoViewed: "También vieron estos productos",
    relatedProducts: "Productos relacionados",
    aiChatTitle: "Asistente de compras con IA",
    aiChatSubtitle: "Hacé preguntas sobre este producto",
    openAIKeyPlaceholder: "Ingresá tu clave de OpenAI (opcional)",
    chatPlaceholder: "Preguntá sobre especificaciones, opiniones, comparaciones...",
    send: "Enviar",
    chatError: "Hubo un error consultando el asistente.",
    freeShippingBadge: "Envío gratis",
    productFeatures: "Lo que tenés que saber de este producto",
    feature1: "Memoria RAM: 8 GB.",
    feature2: "Dispositivo desbloqueado para que elijas tu compañía telefónica preferida.",
    feature3: "Memoria interna de 256 GB.",
    seeFeatures: "Ver características",
    buyingOptions: "Opciones de compra:",
    newProductsFrom: "productos nuevos desde",
    benefit1: "Envío gratis a todo el país",
    benefit2: "Devolución gratis con Mercado Libre",
    unitsAvailable: "unidades disponibles",
    officialStore: "Tienda oficial",
    personalizedAttention: "Atención personalizada",
    officialWarranty: "Garantía oficial de 12 meses",
    electronicInvoice: "Facturación electrónica disponible",
    sellerProducts: "Productos del vendedor",
    knowOtherPayments: "Conocé otros medios de pago",
    alsoViewedFull: "Quienes vieron este producto también compraron",
    screenSize: "Tamaño de la pantalla:",
    screenSmall: "PEQUEÑO",
    screenLarge: "GRANDE",
    capacityTitle: "Capacidad y eficiencia",
    capacityText: "Con un procesador Exynos 1480 y 8 GB de RAM vas a tener un rendimiento excepcional para aplicaciones, juegos y multitarea en Android 14 One UI 6.1.",
    multimediaTitle: "Experiencia multimedia inmersiva",
    multimediaText: "La pantalla Super AMOLED de 6.6\" ofrece colores vivos y contraste intenso con Vision Booster, ideal para ver contenido en exteriores, mientras que Dolby Atmos brinda sonido envolvente.",
    securityTitle: "Seguridad y autonomía",
    securityText: "Incluye lector de huellas en pantalla, Samsung Knox Vault y batería de 5000 mAh con carga rápida de 25 W para que te acompañe todo el día.",
    photoReviews: "Opiniones con fotos",
    sortBy: "Ordenar",
    rating: "Calificación",
    verifiedBadge: "Comprado a Tienda oficial Samsung",
    highlightedReviews: "Opiniones destacadas",
    commentsCount: "comentarios",
    chatWelcome: "Hola, ¿en qué te ayudo? Podés preguntar por características, cámaras, batería o cuotas.",
    chatTip: "💡 Tip:",
    chatTipText: "Ingresá tu OpenAI API Key arriba para respuestas más inteligentes con GPT-4.",
    typing: "Escribiendo",
    average: "promedio",
    ratings: "calificaciones",
    installmentsText: "sin interés",
  },
  pt: {
    loading: "Carregando...",
    searchPlaceholder: "Buscar produtos, marcas e mais...",
    searchButton: "Buscar",
    searching: "Buscando...",
    noResults: "Nenhum resultado encontrado",
    sendTo: "Enviar para:",
    city: "São Paulo",
    breadcrumb1: "Celulares e telefones",
    breadcrumb2: "Acessórios para celulares",
    protectedPurchase: "Compra protegida, receba o produto que esperava ou devolvemos seu dinheiro",
    backToList: "Voltar à listagem",
    breadcrumbCategory: "Celulares e Telefones",
    newProduct: "Novo",
    soldCount: "vendidos",
    stock: "Estoque disponível:",
    units: "unidades",
    quantity: "Quantidade:",
    color: "Cor:",
    blue: "Azul",
    buyNow: "Comprar agora",
    addToCart: "Adicionar ao carrinho",
    freeShipping: "Frete grátis",
    arriving: "Chega",
    tomorrow: "amanhã",
    seeShippingCosts: "Ver como chega",
    soldBy: "Vendido por",
    reputation: "Reputação",
    sales: "vendas",
    returns: "Devolução grátis",
    returnsDesc: "Você tem 30 dias desde que recebe.",
    warranty: "Garantia",
    warrantyDesc: "Compra Protegida com Mercado Pago.",
    securePayment: "Pagamento seguro",
    securePaymentDesc: "Receba o produto que esperava ou devolvemos seu dinheiro.",
    paymentMethods: "Formas de pagamento",
    creditCards: "Cartões de crédito",
    debitCards: "Cartões de débito",
    cash: "Dinheiro",
    installmentsTitle: "Parcelas sem cartão",
    installmentsDesc: "Compre parcelado sem cartão com Mercado Crédito.",
    knowMore: "Saiba mais",
    description: "Descrição",
    specifications: "Características técnicas",
    specRAM: "Memória RAM",
    specStorage: "Armazenamento interno",
    specMainCamera: "Câmera principal",
    specFrontCamera: "Câmera frontal",
    specBattery: "Bateria",
    specProcessor: "Processador",
    specScreen: "Tela",
    specProtection: "Proteção",
    reviewsTitle: "Opiniões do produto",
    overallRating: "Avaliação geral",
    reviews: "opiniões",
    stars: "estrelas",
    reviewBreakdown: "Distribuição de avaliações",
    characteristics: "Características destacadas",
    verifiedPurchase: "Compra verificada",
    alsoViewed: "Também viram estes produtos",
    relatedProducts: "Produtos relacionados",
    aiChatTitle: "Assistente de compras com IA",
    aiChatSubtitle: "Faça perguntas sobre este produto",
    openAIKeyPlaceholder: "Digite sua chave OpenAI (opcional)",
    chatPlaceholder: "Pergunte sobre especificações, opiniões, comparações...",
    send: "Enviar",
    chatError: "Houve um erro ao consultar o assistente.",
    freeShippingBadge: "Frete grátis",
    productFeatures: "O que você precisa saber sobre este produto",
    feature1: "Memória RAM: 8 GB.",
    feature2: "Dispositivo desbloqueado para você escolher sua operadora preferida.",
    feature3: "Memória interna de 256 GB.",
    seeFeatures: "Ver características",
    buyingOptions: "Opções de compra:",
    newProductsFrom: "produtos novos a partir de",
    benefit1: "Frete grátis para todo o país",
    benefit2: "Devolução grátis com Mercado Livre",
    unitsAvailable: "unidades disponíveis",
    officialStore: "Loja oficial",
    personalizedAttention: "Atendimento personalizado",
    officialWarranty: "Garantia oficial de 12 meses",
    electronicInvoice: "Faturamento eletrônico disponível",
    sellerProducts: "Produtos do vendedor",
    knowOtherPayments: "Conheça outras formas de pagamento",
    alsoViewedFull: "Quem viu este produto também comprou",
    screenSize: "Tamanho da tela:",
    screenSmall: "PEQUENO",
    screenLarge: "GRANDE",
    capacityTitle: "Capacidade e eficiência",
    capacityText: "Com um processador Exynos 1480 e 8 GB de RAM você terá um desempenho excepcional para aplicativos, jogos e multitarefas no Android 14 One UI 6.1.",
    multimediaTitle: "Experiência multimídia imersiva",
    multimediaText: "A tela Super AMOLED de 6,6\" oferece cores vivas e contraste intenso com Vision Booster, ideal para visualizar conteúdo ao ar livre, enquanto o Dolby Atmos oferece som envolvente.",
    securityTitle: "Segurança e autonomia",
    securityText: "Inclui leitor de impressão digital na tela, Samsung Knox Vault e bateria de 5000 mAh com carregamento rápido de 25 W para acompanhá-lo o dia todo.",
    photoReviews: "Opiniões com fotos",
    sortBy: "Ordenar",
    rating: "Avaliação",
    verifiedBadge: "Comprado na Loja oficial Samsung",
    highlightedReviews: "Opiniões destacadas",
    commentsCount: "comentários",
    chatWelcome: "Olá, como posso ajudar? Você pode perguntar sobre características, câmeras, bateria ou parcelas.",
    chatTip: "💡 Dica:",
    chatTipText: "Digite sua chave da API OpenAI acima para respostas mais inteligentes com GPT-4.",
    typing: "Digitando",
    average: "média",
    ratings: "avaliações",
    installmentsText: "sem juros",
  },
  en: {
    loading: "Loading...",
    searchPlaceholder: "Search products, brands and more...",
    searchButton: "Search",
    searching: "Searching...",
    noResults: "No results found",
    sendTo: "Ship to:",
    city: "Buenos Aires",
    breadcrumb1: "Cell phones and telephones",
    breadcrumb2: "Cell phone accessories",
    protectedPurchase: "Protected purchase, get the product you expected or we'll refund your money",
    backToList: "Back to listing",
    breadcrumbCategory: "Cell Phones & Telephones",
    newProduct: "New",
    soldCount: "sold",
    stock: "Available stock:",
    units: "units",
    quantity: "Quantity:",
    color: "Color:",
    blue: "Blue",
    buyNow: "Buy now",
    addToCart: "Add to cart",
    freeShipping: "Free shipping",
    arriving: "Arrives",
    tomorrow: "tomorrow",
    seeShippingCosts: "See delivery options",
    soldBy: "Sold by",
    reputation: "Reputation",
    sales: "sales",
    returns: "Free returns",
    returnsDesc: "You have 30 days from receipt.",
    warranty: "Warranty",
    warrantyDesc: "Purchase Protection with Mercado Pago.",
    securePayment: "Secure payment",
    securePaymentDesc: "Get the product you expected or we'll refund your money.",
    paymentMethods: "Payment methods",
    creditCards: "Credit cards",
    debitCards: "Debit cards",
    cash: "Cash",
    installmentsTitle: "Installments without a card",
    installmentsDesc: "Buy in installments without a card with Mercado Crédito.",
    knowMore: "Learn more",
    description: "Description",
    specifications: "Technical specifications",
    specRAM: "RAM Memory",
    specStorage: "Internal storage",
    specMainCamera: "Main camera",
    specFrontCamera: "Front camera",
    specBattery: "Battery",
    specProcessor: "Processor",
    specScreen: "Screen",
    specProtection: "Protection",
    reviewsTitle: "Product reviews",
    overallRating: "Overall rating",
    reviews: "reviews",
    stars: "stars",
    reviewBreakdown: "Rating breakdown",
    characteristics: "Key features",
    verifiedPurchase: "Verified purchase",
    alsoViewed: "Others also viewed these products",
    relatedProducts: "Related products",
    aiChatTitle: "AI Shopping Assistant",
    aiChatSubtitle: "Ask questions about this product",
    openAIKeyPlaceholder: "Enter your OpenAI key (optional)",
    chatPlaceholder: "Ask about specifications, reviews, comparisons...",
    send: "Send",
    chatError: "There was an error consulting the assistant.",
    freeShippingBadge: "Free shipping",
    productFeatures: "What you need to know about this product",
    feature1: "RAM Memory: 8 GB.",
    feature2: "Unlocked device so you can choose your preferred carrier.",
    feature3: "Internal memory of 256 GB.",
    seeFeatures: "See features",
    buyingOptions: "Purchase options:",
    newProductsFrom: "new products from",
    benefit1: "Free shipping nationwide",
    benefit2: "Free returns with Mercado Libre",
    unitsAvailable: "units available",
    officialStore: "Official store",
    personalizedAttention: "Personalized service",
    officialWarranty: "12-month official warranty",
    electronicInvoice: "Electronic invoicing available",
    sellerProducts: "Seller products",
    knowOtherPayments: "Learn about other payment methods",
    alsoViewedFull: "Those who viewed this product also bought",
    screenSize: "Screen size:",
    screenSmall: "SMALL",
    screenLarge: "LARGE",
    capacityTitle: "Capacity and efficiency",
    capacityText: "With an Exynos 1480 processor and 8 GB of RAM you'll have exceptional performance for apps, games and multitasking on Android 14 One UI 6.1.",
    multimediaTitle: "Immersive multimedia experience",
    multimediaText: "The 6.6\" Super AMOLED display offers vivid colors and intense contrast with Vision Booster, ideal for viewing outdoor content, while Dolby Atmos delivers surround sound.",
    securityTitle: "Security and autonomy",
    securityText: "Includes on-screen fingerprint reader, Samsung Knox Vault and 5000 mAh battery with 25W fast charging to keep you going all day.",
    photoReviews: "Reviews with photos",
    sortBy: "Sort",
    rating: "Rating",
    verifiedBadge: "Purchased from Samsung Official Store",
    highlightedReviews: "Featured reviews",
    commentsCount: "comments",
    chatWelcome: "Hello, how can I help you? You can ask about features, cameras, battery or installments.",
    chatTip: "💡 Tip:",
    chatTipText: "Enter your OpenAI API Key above for smarter responses with GPT-4.",
    typing: "Typing",
    average: "average",
    ratings: "ratings",
    installmentsText: "interest-free",
  },
};

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

const currencyFormatter = new Intl.NumberFormat("en-US", {
  style: "currency",
  currency: "USD",
  minimumFractionDigits: 2,
});

const RELATED_PRODUCTS = [
  {
    title: "Samsung Galaxy A55 5G Yellow",
    price: 429,
    image: "/galaxy_a55_amarillo.webp",
    badge: "Free shipping",
  },
  {
    title: "Samsung Galaxy S24 256 GB Gray",
    price: 649,
    image: "/galaxy_s24_gris.webp",
    badge: "Free shipping",
  },
  {
    title: "Samsung Galaxy A55 5G (Back view)",
    price: 429,
    image: "/hero_4.webp",
    badge: "Free shipping",
  },
  {
    title: "Samsung Galaxy A55 5G (Camera detail)",
    price: 429,
    image: "/hero_5.webp",
    badge: "Free shipping",
  },
];

const ALSO_BOUGHT = [
  {
    title: "Samsung Galaxy A55 5G Blue",
    price: 429,
    image: "/hero_1.webp",
  },
  {
    title: "Samsung Galaxy A55 5G Yellow",
    price: 429,
    image: "/galaxy_a55_amarillo.webp",
  },
  {
    title: "Samsung Galaxy S24 256 GB Gray",
    price: 649,
    image: "/galaxy_s24_gris.webp",
  },
  {
    title: "Tecno Spark 20 Pro+",
    price: 215,
    image: "/tecno.webp",
  },
  {
    title: "Samsung Galaxy A55 5G (Side view)",
    price: 429,
    image: "/hero_3.webp",
  },
  {
    title: "Samsung Galaxy A55 5G (Back view)",
    price: 429,
    image: "/hero_4.webp",
  },
  {
    title: "Samsung Galaxy A55 5G (Camera detail)",
    price: 429,
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
  const [language, setLanguage] = useState<Language>('en');
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

  // Get current translations
  const t = translations[language];

  const displayedImage = useMemo(() => {
    if (selectedImage) {
      return selectedImage;
    }
    return item?.images?.[0] || "";
  }, [selectedImage, item]);

  useEffect(() => {
    fetch(`${API_URL}/item?lang=${language}`)
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

    fetch(`${API_URL}/reviews?lang=${language}`)
      .then((res) => res.json())
      .then((data) => {
        setReviews(data);
      })
      .catch((error) => {
        console.error("Failed to load reviews", error);
      });
  }, [language]);

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
        body: JSON.stringify({ question, openai_key: openaiKey || undefined, language })
      });
      const data = await res.json();
      const cleanedAnswer = cleanResponseText(data.answer);
      setChatMessages((m) => [...m, { role: 'bot', text: cleanedAnswer, timestamp: new Date() }]);
    } catch {
      setChatMessages((m) => [...m, { role: 'bot', text: t.chatError, timestamp: new Date() }]);
    } finally {
      setIsTyping(false);
    }
  };

  const formattedPrice = useMemo(() => {
    if (!item) return "";
    return currencyFormatter.format(item.price);
  }, [item]);

  if (!item) {
    return <div>{t.loading}</div>;
  }

  return (
    <>
    <div className={styles.page}>
      <div className={styles.headerWrapper}>
        <header className={styles.banner}>
        <div className={styles.logo}>
          <span className={styles.logoText}>ShopHub</span>
        </div>
          <div className={styles.searchBar}>
            <input 
              type="text" 
              placeholder={t.searchPlaceholder}
              value={searchQuery}
              onChange={(e) => handleSearchInput(e.target.value)}
              onFocus={() => searchResults.length > 0 && setShowSearchResults(true)}
              onBlur={() => setTimeout(() => setShowSearchResults(false), 200)}
            />
            <button type="button" onClick={() => performSearch(searchQuery)}>
              {t.searchButton}
            </button>
            {showSearchResults && (
              <div className={styles.searchDropdown}>
                {isSearching ? (
                  <div className={styles.searchLoading}>{t.searching}</div>
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
                  <div className={styles.searchNoResults}>{t.noResults}</div>
                )}
              </div>
            )}
          </div>
          <div className={styles.location}>
            <span>{t.sendTo}</span>
            <span>{t.city}</span>
          </div>
          <div className={styles.languageSelector}>
            <button 
              onClick={() => setLanguage('es')} 
              className={language === 'es' ? styles.langActive : ''}
              aria-label="Español"
            >
              ES
            </button>
            <button 
              onClick={() => setLanguage('pt')} 
              className={language === 'pt' ? styles.langActive : ''}
              aria-label="Português"
            >
              PT
            </button>
            <button 
              onClick={() => setLanguage('en')} 
              className={language === 'en' ? styles.langActive : ''}
              aria-label="English"
            >
              EN
            </button>
          </div>
        </header>
        <div className={styles.secondaryHeader}>
          <div className={styles.secondaryHeaderContent}>
            <span>{t.breadcrumb1} &gt; {t.breadcrumb2}</span>
            <span>{t.protectedPurchase}</span>
          </div>
        </div>
      </div>

      <main className={styles.main}>
        <div className={styles.mainInner}>
          <nav className={styles.breadcrumbs}>
            <span>{t.backToList}</span>
            <span>&gt;</span>
            <span>{t.breadcrumbCategory}</span>
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
                <span className={styles.secondaryInfo}>{t.newProduct} | {item.reviews_count.toLocaleString()} {t.reviews}</span>
                <h1 className={styles.title}>{item.title}</h1>
                <div className={styles.ratingRow}>
                  <span className={styles.stars}>★★★★★</span>
                  <span>
                    {item.ratings} {t.average} | {item.reviews_count.toLocaleString()} {t.ratings}
                  </span>
                </div>
                <div className={styles.price}>{formattedPrice}</div>
                <span className={styles.installments}>
                  12x {currencyFormatter.format(item.price / 12)} {t.installmentsText}
                </span>

                <div className={styles.colorSection}>
                  <h3>{t.color} <span className={styles.colorName}>{t.blue}</span></h3>
                  <div className={styles.colorOptions}>
                    <div className={styles.colorOption}>
                      <img src="/hero_2.webp" alt={t.blue} className={styles.colorImage} />
                    </div>
                  </div>
                </div>

                <div className={styles.productFeatures}>
                  <h3>{t.productFeatures}</h3>
                  <ul className={styles.featuresList}>
                    <li>{t.feature1}</li>
                    <li>{t.feature2}</li>
                    <li>{t.feature3}</li>
                  </ul>
                  <a 
                    href="#specifications" 
                    className={styles.verCaracteristicas}
                    onClick={(e) => {
                      e.preventDefault();
                      document.getElementById('specifications')?.scrollIntoView({ behavior: 'smooth' });
                    }}
                  >
                    {t.seeFeatures}
                  </a>
                </div>

                <div className={styles.buyingOptions}>
                  <h3>{t.buyingOptions}</h3>
                  <p className={styles.newProductsLink}>
                    <span className={styles.linkText}>5 {t.newProductsFrom}</span> <span className={styles.linkPrice}>$435.00</span>
                  </p>
                </div>
              </div>
              <div className={styles.purchaseActions}>
                <div className={styles.benefits}>
                  <span>{t.benefit1}</span>
                  <span>{t.benefit2}</span>
                  <span>{item.stock} {t.unitsAvailable}</span>
                </div>
                <div className={styles.buttons}>
                  <button className={styles.primaryButton} type="button">
                    {t.buyNow}
                  </button>
                  <button className={styles.secondaryButton} type="button">
                    {t.addToCart}
                  </button>
                </div>

                <div className={styles.sellerInfo}>
                  <div className={styles.sellerHeader}>
                    <div>
                      <p className={styles.sellerName}>{item.seller.name}</p>
                      <p>{item.seller.reputation} Seller</p>
                    </div>
                    <div className={styles.reputation}>
                      <div className={styles.officialStoreBadge}>{t.officialStore}</div>
                      <span>{item.seller.sales.toLocaleString("es-AR")} {t.sales}</span>
                    </div>
                  </div>
                  <ul className={styles.list}>
                    <li>{t.personalizedAttention}</li>
                    <li>{t.officialWarranty}</li>
                    <li>{t.electronicInvoice}</li>
                  </ul>
                </div>

              </div>

              <div className={styles.paymentMethodsBoxSeparate}>
                <h3 className={styles.sectionTitle}>{t.paymentMethods}</h3>
                <div className={styles.paymentSection}>
                  <div className={styles.paymentCategory}>
                    <h4>{t.installmentsTitle}</h4>
                    <div className={styles.paymentLogos}>
                      <img src="/cuotas_sin_tarjeta_logo.png" alt="Mercado Pago" className={styles.paymentLogo} />
                    </div>
                  </div>
                  
                  <div className={styles.paymentCategory}>
                    <h4>{t.creditCards}</h4>
                    <div className={styles.paymentLogos}>
                      <img src="/tarjetas_debido_logos.png" alt={t.creditCards} className={styles.paymentLogo} />
                    </div>
                  </div>

                  <div className={styles.paymentCategory}>
                    <h4>{t.debitCards}</h4>
                    <div className={styles.paymentLogos}>
                      <img src="/tarjetas_debido_logos.png" alt={t.debitCards} className={styles.paymentLogo} />
                    </div>
                  </div>

                  <div className={styles.paymentCategory}>
                    <h4>{t.cash}</h4>
                    <div className={styles.paymentLogos}>
                      <img src="/efectivo_logos.png" alt={t.cash} className={styles.paymentLogo} />
                    </div>
                  </div>

                  <a href="#" className={styles.morePaymentMethods}>{t.knowOtherPayments}</a>
                </div>
              </div>

              <div className={styles.relatedProductsBoxSeparate}>
                <h3 className={styles.sectionTitle}>{t.relatedProducts}</h3>
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
                          <span className={styles.relatedProductBadge}>{t.freeShippingBadge}</span>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            <section className={styles.upperLeftSections}>
              <div className={styles.leftSectionItem}>
                <div className={styles.carouselHeader}>
                  <h2 className={styles.sectionTitle}>{t.alsoViewedFull}</h2>
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
                  <h2 className={styles.sectionTitle}>{t.sellerProducts}</h2>
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
              <h2 className={styles.sectionTitle}>{t.specifications}</h2>
              
              <div className={styles.screenSizeGraphic}>
                <div className={styles.screenSizeIcon}>
                  <div className={styles.screenIcon}>📱</div>
                </div>
                <div className={styles.screenSizeInfo}>
                  <div className={styles.screenSizeText}>
                    {t.screenSize} <strong>6.6&quot;</strong>
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
                      <span className={styles.barLabelSmall}>{t.screenSmall}</span>
                      <span className={styles.barLabelLarge}>{t.screenLarge}</span>
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
              <h2 className={styles.sectionTitle}>{t.description}</h2>
              <p>{item.description}</p>
              <p className={styles.highlight}>{t.capacityTitle}</p>
              <p>
                {t.capacityText}
              </p>
                <p className={styles.highlight}>{t.multimediaTitle}</p>
              <p>
                {t.multimediaText}
              </p>
              <p className={styles.highlight}>{t.securityTitle}</p>
              <p>
                {t.securityText}
              </p>
              </div>

              {reviews && (
                <div className={styles.leftSectionItem}>
                  <h2 className={styles.sectionTitle}>{t.reviewsTitle}</h2>
                  
                  <div className={styles.reviewsContainer}>
                    <div className={styles.reviewsLeft}>
                      <div className={styles.overallRating}>
                        <div className={styles.ratingNumber}>{reviews.overall_rating}</div>
                        <div className={styles.starsContainer}>
                          {[...Array(5)].map((_, i) => (
                            <span key={i} className={styles.star}>★</span>
                          ))}
                        </div>
                        <div className={styles.totalReviews}>{reviews.total_reviews} {t.reviews}</div>
                      </div>


                      <div className={styles.characteristicRatings}>
                        <h3 className={styles.characteristicTitle}>{t.characteristics}</h3>
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
                        <h3 className={styles.photoReviewsTitle}>{t.photoReviews}</h3>
                        <div className={styles.photoThumbnails}>
                          {[1, 2, 3, 4].map((photoNum) => (
                            <div key={photoNum} className={styles.photoThumbnail}>
                              <img src={`/opinion_photo_${photoNum}.webp`} alt={`Review photo ${photoNum}`} />
                              <div className={styles.photoRating}>5 ★</div>
                            </div>
                          ))}
                        </div>
                        <div className={styles.reviewFilters}>
                          <div className={styles.filterButton}>{t.sortBy}</div>
                          <div className={styles.filterButton}>{t.rating}</div>
                        </div>
                        <div className={styles.verifiedBadge}>
                          <span className={styles.checkmark}>✓</span>
                          {t.verifiedBadge}
                        </div>
                      </div>

                      <div className={styles.highlightedReviews}>
                        <h3 className={styles.highlightedTitle}>{t.highlightedReviews}</h3>
                        <div className={styles.commentCount}>122 {t.commentsCount}</div>
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
    <button className={styles.chatFab} onClick={() => setChatOpen((v) => !v)} aria-label={t.aiChatTitle}>
      {chatOpen ? '×' : '?'}
    </button>
    {chatOpen && (
      <div className={styles.chatPanel}>
        <div className={styles.chatHeader}>{t.aiChatTitle}</div>
        <div className={styles.apiKeyRow}>
          <input 
            type="password"
            value={openaiKey} 
            onChange={(e) => setOpenaiKey(e.target.value)} 
            placeholder={t.openAIKeyPlaceholder}
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
                <span>{t.typing}</span>
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
              {t.chatWelcome}
              {!openaiKey && <><br/><br/><strong>{t.chatTip}</strong> {t.chatTipText}</>}
            </div>
          )}
        </div>
        <div className={styles.chatInputRow}>
          <input 
            value={chatInput} 
            onChange={(e) => setChatInput(e.target.value)} 
            placeholder={t.chatPlaceholder}
            onKeyDown={(e) => { if (e.key === 'Enter' && !isTyping) sendChat(); }} 
            disabled={isTyping}
          />
          <button onClick={sendChat} disabled={isTyping || !chatInput.trim()}>
            {isTyping ? t.searching : t.send}
          </button>
        </div>
    </div>
    )}
    </>
  );
}
