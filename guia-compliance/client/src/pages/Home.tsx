/*
 * DESIGN: "Legal Navigator" — Editorial Magazine + Legal Documentation
 * Palette: Cream bg (#F5F0E8), Forest Green (#1C3B2D), Golden Mustard (#C9A227)
 * Typography: Playfair Display (headings) + Lato (body)
 * Layout: Magazine editorial with pull quotes, marginal notes, legal citations
 */

import { useState, useEffect, useRef } from "react";
import { toast } from "sonner";
import {
  CheckCircle,
  XCircle,
  AlertTriangle,
  Copy,
  ChevronDown,
  ChevronUp,
  BookOpen,
  Shield,
  Instagram,
  Scale,
  FileText,
  ExternalLink,
  TrendingUp,
  Users,
  AlertCircle,
  Info,
} from "lucide-react";

// ─── Types ───────────────────────────────────────────────────────────────────
type StatusType = "safe" | "warning" | "danger";

interface RuleItem {
  title: string;
  description: string;
  status: StatusType;
  detail?: string;
}

interface AccordionItem {
  question: string;
  answer: string;
}

// ─── Data ────────────────────────────────────────────────────────────────────
const cvmRules: RuleItem[] = [
  {
    title: "Compartilhar resultados reais com contexto educacional",
    status: "safe",
    description:
      "Você pode mostrar prints de operações reais desde que o foco seja pedagógico: explicar o raciocínio da entrada, o gerenciamento de risco, os erros cometidos e as lições aprendidas.",
    detail:
      "A CVM distingue educação financeira de recomendação de investimento. O conteúdo educacional não exige habilitação, desde que não haja cobrança de mensalidade, não seja habitual com viés de recomendação e não use linguagem apelativa para induzir terceiros.",
  },
  {
    title: "Usar disclaimer claro em todos os posts",
    status: "safe",
    description:
      'Sempre incluir aviso explícito de que o conteúdo é exclusivamente educacional e não constitui recomendação de compra ou venda de ativos.',
    detail:
      "Segundo a ANBIMA e a CVM, o disclaimer por si só não é suficiente para descaracterizar uma recomendação se o conteúdo for habitual, remunerado e apelativo. Mas é um elemento essencial de boa-fé e transparência.",
  },
  {
    title: "Diário de operações sem cobrança de acesso",
    status: "safe",
    description:
      "Compartilhar seu diário de forma gratuita, sem assinaturas, mensalidades ou taxas de adesão, reduz significativamente o risco de ser enquadrado como analista de valores mobiliários não habilitado.",
    detail:
      "A Resolução CVM nº 20/2021 define como analista profissional quem exerce a atividade de forma habitual, com caráter profissional e remuneratório. A ausência de remuneração é um fator relevante na análise.",
  },
  {
    title: "Cobrar mensalidade ou assinatura pelo conteúdo",
    status: "danger",
    description:
      "Criar grupos pagos, assinaturas ou qualquer forma de remuneração direta pelo acesso ao diário de operações caracteriza atividade regulada pela CVM.",
    detail:
      "A CVM considera que a cobrança de mensalidade ou anuidade é um dos principais indicadores de exercício profissional de análise de valores mobiliários, exigindo habilitação CNPI pela APIMEC.",
  },
  {
    title: "Usar linguagem apelativa ou promessas de ganho",
    status: "danger",
    description:
      'Frases como "garanto X% ao mês", "estratégia infalível", "todo mundo consegue" ou "siga minhas operações" configuram linguagem de indução e podem ser interpretadas como exercício irregular.',
    detail:
      "O regulador monitora a linguagem utilizada. Conteúdo apelativo que tenta convencer ou induzir investidores é atividade exclusiva de profissionais credenciados, sujeita a penalidades e ao crime previsto no art. 27-E da Lei nº 6.385/76.",
  },
  {
    title: "Recomendar explicitamente compra ou venda de ativos",
    status: "danger",
    description:
      'Dizer "compre PETR4 agora", "venda essa opção hoje" ou qualquer instrução direta de operação para seus seguidores é recomendação de investimento e exige habilitação.',
    detail:
      "Mesmo sem cobrança, a recomendação habitual e explícita de ativos pode configurar exercício irregular da atividade de analista. O crime previsto no art. 27-E da Lei nº 6.385/76 pode ser aplicado mesmo a título gratuito.",
  },
  {
    title: "Publicações frequentes com análise habitual",
    status: "warning",
    description:
      "A frequência e habitualidade das publicações é um dos critérios usados pela CVM para avaliar se a atividade tem caráter profissional.",
    detail:
      "Não há um número definido de posts que automaticamente caracterize a atividade como profissional, mas a combinação de frequência + linguagem de recomendação + remuneração é o que a CVM avalia em conjunto.",
  },
  {
    title: "Mostrar operações que você já realizou (passado)",
    status: "safe",
    description:
      "Documentar operações já encerradas, com análise do que funcionou e do que não funcionou, é claramente educacional e não configura recomendação prospectiva.",
    detail:
      "O diário retrospectivo é a forma mais segura de compartilhar operações. Você está ensinando com base em experiência própria, não direcionando decisões futuras de terceiros.",
  },
];

const metaRules: RuleItem[] = [
  {
    title: "Conteúdo educacional sobre mercado financeiro",
    status: "safe",
    description:
      "O Instagram e o Facebook permitem conteúdo educacional sobre finanças, investimentos e trading, desde que não promova produtos financeiros não autorizados ou esquemas fraudulentos.",
    detail:
      "A Meta classifica serviços financeiros como categoria restrita para anúncios pagos, mas conteúdo orgânico educacional é permitido. A restrição mais severa aplica-se a anúncios, não a posts comuns.",
  },
  {
    title: "Mostrar prints de ganhos sem contexto educativo",
    status: "danger",
    description:
      "Posts com apenas prints de lucros, sem explicação educacional, podem ser interpretados pelo algoritmo como promoção de esquema de enriquecimento rápido e resultar em remoção ou suspensão.",
    detail:
      "O Instagram usa algoritmos para detectar padrões de conteúdo. Posts que parecem promover ganhos fáceis, mesmo sem intenção, podem acionar filtros automáticos de moderação.",
  },
  {
    title: "Usar palavras como 'garanto', 'certeza', 'todo mundo consegue'",
    status: "danger",
    description:
      "Essas expressões são detectadas pelos sistemas de moderação como indicadores de conteúdo enganoso ou de esquemas financeiros fraudulentos.",
    detail:
      "O algoritmo da Meta interpreta o conteúdo de forma automatizada. Um erro de comunicação pode custar a conta, mesmo sem intenção de fraude. O Instagram pode suspender contas sem aviso prévio.",
  },
  {
    title: "Prometer resultado financeiro específico sem disclaimer",
    status: "danger",
    description:
      "Qualquer promessa de retorno específico sem aviso legal claro viola as políticas de publicidade da Meta e pode resultar em remoção de conteúdo.",
  },
  {
    title: "Incluir disclaimer em todos os posts financeiros",
    status: "safe",
    description:
      "Adicionar aviso claro de que o conteúdo é educacional e não constitui recomendação de investimento protege tanto contra ações da CVM quanto contra moderação do Instagram.",
  },
  {
    title: "Identificar parcerias comerciais com #Publi ou #ParceriaPaga",
    status: "safe",
    description:
      "Se você tiver qualquer parceria com instituição financeira, é obrigatório identificar o conteúdo como publicidade, tanto pelas regras da ANBIMA quanto pelas políticas da Meta.",
    detail:
      "A falta de identificação de publicidade pode resultar em penalidades para a instituição contratante (que é fiscalizada pela ANBIMA) e em remoção do conteúdo pela Meta.",
  },
  {
    title: "Conteúdo sobre criptomoedas e ativos de alto risco",
    status: "warning",
    description:
      "A Meta tem restrições específicas para conteúdo sobre criptomoedas, especialmente para anúncios. Conteúdo orgânico educacional é geralmente permitido, mas requer atenção redobrada.",
    detail:
      "Para anúncios pagos sobre criptomoedas, a Meta exige autorização prévia. Para conteúdo orgânico, o risco é menor, mas o disclaimer sobre riscos é especialmente importante nessa categoria.",
  },
];

const bestPractices: AccordionItem[] = [
  {
    question: "Como estruturar um post de diário de operações de forma segura?",
    answer:
      "Estruture o post em três partes: (1) Contexto da operação — qual era o cenário de mercado, qual foi o raciocínio para entrar na operação, qual era o plano de gerenciamento de risco; (2) Resultado — o que aconteceu, o que funcionou, o que não funcionou; (3) Aprendizado — qual lição pode ser extraída. Sempre termine com o disclaimer padrão. Evite frases no imperativo ('compre', 'venda') e prefira o passado ('entrei', 'saí', 'aprendi').",
  },
  {
    question: "Qual é o disclaimer ideal para posts de operações com opções?",
    answer:
      "Um disclaimer robusto deve conter: (1) declaração de que o conteúdo é exclusivamente educacional; (2) declaração de que não constitui recomendação de compra ou venda de ativos; (3) aviso de que operações com opções envolvem risco de perda total do capital investido; (4) recomendação para que o leitor consulte um profissional habilitado antes de tomar decisões de investimento. Veja o modelo pronto na seção 'Disclaimers Prontos' abaixo.",
  },
  {
    question: "Posso mostrar minha carteira atual e operações abertas?",
    answer:
      "Mostrar operações abertas é mais arriscado do que mostrar operações encerradas, pois pode ser interpretado como sinalização de compra/venda em tempo real. Se optar por fazê-lo, deixe muito claro que está documentando para fins educacionais e que não está fazendo recomendação. Prefira sempre o formato retrospectivo (operações já encerradas) para minimizar riscos.",
  },
  {
    question: "Posso criar um grupo no WhatsApp ou Telegram para compartilhar operações?",
    answer:
      "Grupos gratuitos com foco educacional têm menor risco, mas a combinação de grupo + operações em tempo real + linguagem de recomendação pode ser interpretada como atividade de analista não habilitado. Grupos pagos são claramente problemáticos. Se criar um grupo, mantenha o foco em discussão educacional, não em sinais de operação.",
  },
  {
    question: "Como a CVM monitora influenciadores financeiros?",
    answer:
      "A CVM firmou convênio com a ANBIMA em 2021 para compartilhamento de monitoramento de influenciadores. A ANBIMA utiliza robôs e inteligência artificial para monitorar publicações sobre finanças e investimentos 24/7 nas redes sociais. A CVM também monitora movimentos de mercado para identificar possível manipulação de preços. Em 2026, a CVM incluiu a regulamentação de finfluencers em sua agenda regulatória.",
  },
  {
    question: "Quais são as penalidades por exercício irregular de atividade regulada?",
    answer:
      "O art. 27-E da Lei nº 6.385/76 tipifica o crime de exercício irregular de atividades no mercado de valores mobiliários, com pena de reclusão de 1 a 4 anos e multa. A CVM também pode aplicar multas administrativas de até R$ 50 milhões ou 3 vezes o valor da vantagem obtida. Além disso, a conta no Instagram/Facebook pode ser suspensa.",
  },
  {
    question: "Preciso de alguma certificação para criar conteúdo educacional?",
    answer:
      "Para conteúdo puramente educacional e gratuito, sem recomendação de ativos específicos, não há exigência de certificação. No entanto, ter uma certificação (como CPA-20, CEA ou CFP) aumenta sua credibilidade e demonstra comprometimento com o conhecimento técnico. Se quiser analisar ativos e fazer recomendações, a certificação CNPI pela APIMEC é obrigatória.",
  },
  {
    question: "O que fazer se minha conta for suspensa pelo Instagram?",
    answer:
      "Acesse o Central de Ajuda do Instagram e solicite revisão da decisão. Explique que seu conteúdo é educacional e apresente evidências (disclaimers, histórico de posts). Se a suspensão for relacionada a conteúdo financeiro, revise todos os posts e remova aqueles que possam ter linguagem apelativa ou promessas de ganho. Considere consultar um advogado especializado em Direito Digital.",
  },
];

const disclaimerTemplates = [
  {
    title: "Disclaimer Padrão (Curto)",
    text: "⚠️ DISCLAIMER: Este conteúdo é exclusivamente educacional e não constitui recomendação de compra ou venda de ativos. Operações com opções envolvem risco de perda total do capital. Consulte um profissional habilitado antes de investir.",
  },
  {
    title: "Disclaimer Completo (Para Posts Detalhados)",
    text: "⚠️ AVISO LEGAL: Este conteúdo tem finalidade exclusivamente educacional e representa minha experiência pessoal como operador de opções com capital próprio. Não constitui recomendação de investimento, análise de valores mobiliários ou qualquer forma de consultoria financeira. Resultados passados não garantem resultados futuros. Operações com derivativos envolvem risco elevado, incluindo perda total do capital investido. Cada investidor possui perfil e objetivos distintos. Antes de tomar qualquer decisão de investimento, consulte um analista de valores mobiliários habilitado (CNPI) ou consultor de investimentos registrado na CVM.",
  },
  {
    title: "Disclaimer para Stories/Reels (Ultra Curto)",
    text: "📚 Conteúdo educacional. Não é recomendação de investimento. Risco de perda total.",
  },
];

// ─── Sub-components ───────────────────────────────────────────────────────────

function StatusIcon({ status }: { status: StatusType }) {
  if (status === "safe")
    return <CheckCircle className="w-5 h-5 text-[#1A7A4A] flex-shrink-0" />;
  if (status === "warning")
    return <AlertTriangle className="w-5 h-5 text-[#C47A00] flex-shrink-0" />;
  return <XCircle className="w-5 h-5 text-[#B52B2B] flex-shrink-0" />;
}

function StatusBadge({ status }: { status: StatusType }) {
  const map = {
    safe: { label: "Permitido", cls: "badge-safe" },
    warning: { label: "Atenção", cls: "badge-warning" },
    danger: { label: "Proibido", cls: "badge-danger" },
  };
  const { label, cls } = map[status];
  return <span className={cls}>{label}</span>;
}

function RuleCard({ rule }: { rule: RuleItem }) {
  const [open, setOpen] = useState(false);
  const cardClass =
    rule.status === "safe"
      ? "rule-card-safe"
      : rule.status === "warning"
      ? "rule-card-warning"
      : "rule-card-danger";

  return (
    <div className={`${cardClass} mb-3 transition-all duration-200 hover:shadow-md`}>
      <div
        className="flex items-start gap-3 cursor-pointer"
        onClick={() => setOpen(!open)}
      >
        <StatusIcon status={rule.status} />
        <div className="flex-1 min-w-0">
          <div className="flex items-start justify-between gap-2 flex-wrap">
            <p className="font-semibold text-[#1A1A1A] text-sm leading-snug flex-1">
              {rule.title}
            </p>
            <div className="flex items-center gap-2 flex-shrink-0">
              <StatusBadge status={rule.status} />
              {rule.detail && (
                <button className="text-[#4A4A4A] hover:text-[#1C3B2D] transition-colors">
                  {open ? (
                    <ChevronUp className="w-4 h-4" />
                  ) : (
                    <ChevronDown className="w-4 h-4" />
                  )}
                </button>
              )}
            </div>
          </div>
          <p className="text-[#4A4A4A] text-sm mt-1 leading-relaxed">
            {rule.description}
          </p>
          {open && rule.detail && (
            <div className="mt-3 pt-3 border-t border-gray-100">
              <p className="text-[#4A4A4A] text-sm leading-relaxed italic">
                {rule.detail}
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

function AccordionCard({ item, index }: { item: AccordionItem; index: number }) {
  const [open, setOpen] = useState(false);
  return (
    <div className="border border-[#D4CFC5] rounded-lg overflow-hidden mb-3 bg-white">
      <button
        className="w-full flex items-center justify-between p-4 text-left hover:bg-[#F5F0E8] transition-colors"
        onClick={() => setOpen(!open)}
      >
        <div className="flex items-start gap-3">
          <span className="text-[#C9A227] font-bold text-sm font-mono flex-shrink-0 mt-0.5">
            {String(index + 1).padStart(2, "0")}
          </span>
          <span
            className="font-semibold text-[#1C3B2D] text-sm leading-snug"
            style={{ fontFamily: "'Playfair Display', serif" }}
          >
            {item.question}
          </span>
        </div>
        {open ? (
          <ChevronUp className="w-4 h-4 text-[#4A4A4A] flex-shrink-0 ml-2" />
        ) : (
          <ChevronDown className="w-4 h-4 text-[#4A4A4A] flex-shrink-0 ml-2" />
        )}
      </button>
      {open && (
        <div className="px-4 pb-4 pt-0">
          <div className="ml-7 text-[#4A4A4A] text-sm leading-relaxed border-t border-[#EDE8DC] pt-3">
            {item.answer}
          </div>
        </div>
      )}
    </div>
  );
}

function DisclaimerCard({ template }: { template: (typeof disclaimerTemplates)[0] }) {
  const handleCopy = () => {
    navigator.clipboard.writeText(template.text).then(() => {
      toast.success("Disclaimer copiado para a área de transferência!");
    });
  };

  return (
    <div className="mb-4">
      <div className="flex items-center justify-between mb-2">
        <h4
          className="font-semibold text-[#1C3B2D] text-sm"
          style={{ fontFamily: "'Playfair Display', serif" }}
        >
          {template.title}
        </h4>
        <button
          onClick={handleCopy}
          className="flex items-center gap-1.5 text-xs text-[#C9A227] hover:text-[#A07A10] font-semibold transition-colors border border-[#C9A227] hover:border-[#A07A10] px-3 py-1 rounded-full"
        >
          <Copy className="w-3 h-3" />
          Copiar
        </button>
      </div>
      <div className="disclaimer-box">
        <p className="text-sm leading-relaxed">{template.text}</p>
      </div>
    </div>
  );
}

// ─── Main Component ───────────────────────────────────────────────────────────
export default function Home() {
  const [activeSection, setActiveSection] = useState("cvm");
  const [scrolled, setScrolled] = useState(false);
  const observerRef = useRef<IntersectionObserver | null>(null);

  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 60);
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  // Fade-in on scroll
  useEffect(() => {
    observerRef.current = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("visible");
          }
        });
      },
      { threshold: 0.1 }
    );

    document.querySelectorAll(".fade-in-up").forEach((el) => {
      observerRef.current?.observe(el);
    });

    return () => observerRef.current?.disconnect();
  }, []);

  const scrollTo = (id: string) => {
    const el = document.getElementById(id);
    if (el) {
      const offset = 80;
      const top = el.getBoundingClientRect().top + window.scrollY - offset;
      window.scrollTo({ top, behavior: "smooth" });
      setActiveSection(id);
    }
  };

  const navItems = [
    { id: "cvm", label: "§1 CVM", icon: Scale },
    { id: "meta", label: "§2 Instagram/Meta", icon: Instagram },
    { id: "praticas", label: "§3 Boas Práticas", icon: BookOpen },
    { id: "disclaimers", label: "§4 Disclaimers", icon: FileText },
    { id: "checklist", label: "§5 Checklist", icon: Shield },
  ];

  const checklistItems = [
    { text: "O conteúdo foca em educação, não em recomendação de ativos específicos", category: "cvm" },
    { text: "Não há cobrança de mensalidade, assinatura ou taxa pelo conteúdo", category: "cvm" },
    { text: "A linguagem é descritiva (passado) e não imperativa (compre/venda)", category: "cvm" },
    { text: "Não há promessas de rentabilidade ou garantia de resultados", category: "cvm" },
    { text: "O disclaimer está incluído de forma clara e visível no post", category: "meta" },
    { text: "Não há palavras como 'garanto', 'certeza' ou 'infalível'", category: "meta" },
    { text: "Prints de ganhos têm contexto educacional explicativo", category: "meta" },
    { text: "Parcerias comerciais estão identificadas com #Publi ou #ParceriaPaga", category: "meta" },
    { text: "O post explica o raciocínio da operação, não apenas o resultado", category: "pratica" },
    { text: "Há menção ao risco envolvido na operação", category: "pratica" },
  ];

  const [checked, setChecked] = useState<boolean[]>(
    new Array(checklistItems.length).fill(false)
  );

  const toggleCheck = (i: number) => {
    const next = [...checked];
    next[i] = !next[i];
    setChecked(next);
  };

  const checkedCount = checked.filter(Boolean).length;
  const progress = Math.round((checkedCount / checklistItems.length) * 100);

  return (
    <div className="min-h-screen" style={{ backgroundColor: "#F5F0E8" }}>
      {/* ── Sticky Nav ── */}
      <nav
        className={`sticky-nav transition-shadow duration-300 ${
          scrolled ? "shadow-md" : ""
        }`}
      >
        <div className="container">
          <div className="flex items-center justify-between py-3">
            <div className="flex items-center gap-2">
              <Scale className="w-5 h-5 text-[#1C3B2D]" />
              <span
                className="font-bold text-[#1C3B2D] text-sm hidden sm:block"
                style={{ fontFamily: "'Playfair Display', serif" }}
              >
                Guia de Compliance
              </span>
            </div>
            <div className="flex items-center gap-1 overflow-x-auto">
              {navItems.map(({ id, label }) => (
                <button
                  key={id}
                  onClick={() => scrollTo(id)}
                  className={`px-3 py-1.5 text-xs font-semibold rounded-full transition-all whitespace-nowrap ${
                    activeSection === id
                      ? "bg-[#1C3B2D] text-[#F5F0E8]"
                      : "text-[#4A4A4A] hover:text-[#1C3B2D] hover:bg-[#E8F0EB]"
                  }`}
                >
                  {label}
                </button>
              ))}
            </div>
          </div>
        </div>
      </nav>

      {/* ── Hero ── */}
      <section className="relative overflow-hidden">
        <div
          className="absolute inset-0 bg-cover bg-center"
          style={{
            backgroundImage: `url(https://d2xsxph8kpxj0f.cloudfront.net/310519663645047679/igKY7aJWtZm3BzyexY6MqN/hero-compliance-ch9C4qjSoeZoKozcncfHY2.webp)`,
          }}
        />
        <div className="absolute inset-0 bg-gradient-to-r from-[#1C3B2D]/90 via-[#1C3B2D]/70 to-transparent" />
        <div className="relative container py-20 lg:py-28">
          <div className="max-w-2xl">
            <div className="flex items-center gap-2 mb-4">
              <span className="section-number" style={{ color: "#C9A227" }}>
                Guia Completo
              </span>
            </div>
            <h1
              className="text-4xl lg:text-5xl xl:text-6xl font-bold text-white leading-tight mb-6"
              style={{ fontFamily: "'Playfair Display', serif" }}
            >
              Diário de Operações
              <span className="block text-[#F0D98A] italic">com Segurança Legal</span>
            </h1>
            <p className="text-lg text-white/85 leading-relaxed mb-8 max-w-xl">
              Como compartilhar suas operações com opções de forma educacional no
              Instagram e Facebook sem violar as regras da CVM nem arriscar a
              suspensão da sua conta.
            </p>
            <div className="flex flex-wrap gap-3">
              <button
                onClick={() => scrollTo("cvm")}
                className="bg-[#C9A227] hover:bg-[#A07A10] text-[#1A1A1A] font-bold px-6 py-3 rounded-lg transition-colors text-sm"
              >
                Ver Regras da CVM
              </button>
              <button
                onClick={() => scrollTo("disclaimers")}
                className="border-2 border-white/60 hover:border-white text-white font-semibold px-6 py-3 rounded-lg transition-colors text-sm"
              >
                Pegar Disclaimers Prontos
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* ── Alert Banner ── */}
      <div className="bg-[#1C3B2D] text-white py-4">
        <div className="container">
          <div className="flex items-center gap-3 flex-wrap">
            <AlertCircle className="w-5 h-5 text-[#C9A227] flex-shrink-0" />
            <p className="text-sm">
              <strong>Atualização 2026:</strong> A CVM incluiu a regulamentação de
              finfluencers em sua agenda regulatória para 2026. As regras podem
              mudar — mantenha-se atualizado.
            </p>
            <a
              href="https://finsidersbrasil.com.br/regulamentacao/cvm-lanca-agenda-regulatoria-de-2026-com-foco-em-crowdfunding-e-mercados-menores/"
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-1 text-[#C9A227] text-xs font-semibold hover:underline ml-auto flex-shrink-0"
            >
              Saiba mais <ExternalLink className="w-3 h-3" />
            </a>
          </div>
        </div>
      </div>

      {/* ── Stats Row ── */}
      <div className="bg-white border-b border-[#D4CFC5]">
        <div className="container py-6">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
            {[
              { icon: Scale, value: "Res. CVM 20/2021", label: "Regula analistas de valores" },
              { icon: AlertTriangle, value: "Art. 27-E", label: "Crime de exercício irregular" },
              { icon: Users, value: "24/7", label: "Monitoramento ANBIMA/CVM" },
              { icon: TrendingUp, value: "2026", label: "Regulação de finfluencers prevista" },
            ].map(({ icon: Icon, value, label }) => (
              <div key={label} className="text-center">
                <Icon className="w-6 h-6 text-[#C9A227] mx-auto mb-2" />
                <div
                  className="font-bold text-[#1C3B2D] text-sm"
                  style={{ fontFamily: "'Playfair Display', serif" }}
                >
                  {value}
                </div>
                <div className="text-xs text-[#4A4A4A] mt-0.5">{label}</div>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="container py-12">
        <div className="max-w-4xl mx-auto">

          {/* ── Section 1: CVM ── */}
          <section id="cvm" className="mb-16 fade-in-up">
            <div className="flex items-start gap-4 mb-6">
              <div className="w-12 h-12 bg-[#1C3B2D] rounded-lg flex items-center justify-center flex-shrink-0">
                <Scale className="w-6 h-6 text-[#C9A227]" />
              </div>
              <div>
                <span className="section-number">§1</span>
                <h2
                  className="text-2xl lg:text-3xl font-bold text-[#1C3B2D] mt-1"
                  style={{ fontFamily: "'Playfair Display', serif" }}
                >
                  Regras da CVM
                </h2>
                <p className="text-[#4A4A4A] text-sm mt-1">
                  Comissão de Valores Mobiliários — Regulação do Mercado de Capitais
                </p>
              </div>
            </div>

            <div className="grid md:grid-cols-5 gap-6 mb-8">
              <div className="md:col-span-3">
                <p className="text-[#4A4A4A] leading-relaxed mb-4">
                  A CVM regula quem pode analisar e recomendar valores mobiliários no Brasil.
                  A fronteira entre <strong>educação financeira</strong> e{" "}
                  <strong>exercício irregular de atividade regulada</strong> é definida por três
                  critérios principais: caráter profissional, habitualidade e remuneração.
                </p>
                <div className="pull-quote">
                  "Finfluencers podem produzir conteúdo sobre investimentos nas redes sociais,
                  desde que não desempenhem atividades que dependam de habilitação ou autorização
                  da CVM."
                  <div className="text-xs text-[#4A4A4A] mt-2 not-italic font-normal" style={{ fontFamily: "'Lato', sans-serif" }}>
                    — Consultor Jurídico, Dez/2025
                  </div>
                </div>
              </div>
              <div className="md:col-span-2">
                <img
                  src="https://d2xsxph8kpxj0f.cloudfront.net/310519663645047679/igKY7aJWtZm3BzyexY6MqN/cvm-section-XFFvWFFXhwgBMmJTF9e5W8.webp"
                  alt="Regulação financeira"
                  className="w-full rounded-lg shadow-md object-cover"
                  style={{ maxHeight: "220px" }}
                />
              </div>
            </div>

            <div className="legal-cite mb-6">
              <strong>Resolução CVM nº 20/2021</strong> — Atividade de analista de valores
              mobiliários exige habilitação quando há:{"\n"}
              (1) benefício ou remuneração pela oferta de recomendações;{"\n"}
              (2) cobrança de mensalidades ou anuidades;{"\n"}
              (3) publicações frequentes e realizadas de forma habitual.{"\n\n"}
              <strong>Art. 27-E da Lei nº 6.385/76</strong> — Exercer atividade de analista
              de valores mobiliários sem autorização: reclusão de 1 a 4 anos e multa,
              mesmo a título gratuito.
            </div>

            <div className="space-y-1">
              {cvmRules.map((rule, i) => (
                <RuleCard key={i} rule={rule} />
              ))}
            </div>

            <div className="mt-6 p-4 bg-[#E8F0EB] rounded-lg border border-[#1A7A4A]/20">
              <div className="flex items-start gap-3">
                <Info className="w-5 h-5 text-[#1A7A4A] flex-shrink-0 mt-0.5" />
                <div>
                  <p className="font-semibold text-[#1C3B2D] text-sm">
                    Zona Cinzenta Regulatória
                  </p>
                  <p className="text-[#4A4A4A] text-sm mt-1 leading-relaxed">
                    A própria CVM reconheceu a "zona de incerteza" na Consulta Pública SDM nº
                    04/2023. Até que uma regulação específica para finfluencers seja publicada,
                    a fronteira entre o lícito e o ilícito permanece nebulosa. A melhor
                    estratégia é manter-se claramente no campo educacional.
                  </p>
                </div>
              </div>
            </div>
          </section>

          {/* ── Section 2: Meta/Instagram ── */}
          <section id="meta" className="mb-16 fade-in-up">
            <div className="flex items-start gap-4 mb-6">
              <div className="w-12 h-12 bg-[#1C3B2D] rounded-lg flex items-center justify-center flex-shrink-0">
                <Instagram className="w-6 h-6 text-[#C9A227]" />
              </div>
              <div>
                <span className="section-number">§2</span>
                <h2
                  className="text-2xl lg:text-3xl font-bold text-[#1C3B2D] mt-1"
                  style={{ fontFamily: "'Playfair Display', serif" }}
                >
                  Políticas do Instagram e Facebook
                </h2>
                <p className="text-[#4A4A4A] text-sm mt-1">
                  Meta Platforms — Padrões da Comunidade e Políticas de Publicidade
                </p>
              </div>
            </div>

            <div className="grid md:grid-cols-5 gap-6 mb-8">
              <div className="md:col-span-3">
                <p className="text-[#4A4A4A] leading-relaxed mb-4">
                  A Meta classifica serviços financeiros como <strong>categoria restrita</strong>{" "}
                  para anúncios pagos, mas conteúdo orgânico educacional é geralmente permitido.
                  O risco maior está na moderação algorítmica, que pode interpretar padrões de
                  linguagem como indicadores de fraude financeira.
                </p>
                <div className="pull-quote">
                  "O Instagram interpreta o conteúdo por algoritmo. Um erro de comunicação
                  custa sua conta."
                  <div className="text-xs text-[#4A4A4A] mt-2 not-italic font-normal" style={{ fontFamily: "'Lato', sans-serif" }}>
                    — @erikacaccia.adv, Advogada Digital
                  </div>
                </div>
              </div>
              <div className="md:col-span-2">
                <img
                  src="https://d2xsxph8kpxj0f.cloudfront.net/310519663645047679/igKY7aJWtZm3BzyexY6MqN/social-media-section-ZPnzgUmfMNY6T5bu2TPEti.webp"
                  alt="Redes sociais e finanças"
                  className="w-full rounded-lg shadow-md object-cover"
                  style={{ maxHeight: "220px" }}
                />
              </div>
            </div>

            <div className="legal-cite mb-6">
              <strong>Meta — Padrões da Comunidade</strong> — Conteúdo financeiro proibido:{"\n"}
              • Esquemas de enriquecimento rápido e pirâmides financeiras;{"\n"}
              • Promessas de retorno garantido sem base factual;{"\n"}
              • Conteúdo que induz ao erro sobre produtos financeiros.{"\n\n"}
              <strong>Meta — Publicidade Restrita</strong> — Serviços financeiros (incluindo
              opções, derivativos e criptomoedas) exigem aprovação prévia para anúncios pagos.
            </div>

            <div className="space-y-1">
              {metaRules.map((rule, i) => (
                <RuleCard key={i} rule={rule} />
              ))}
            </div>
          </section>

          {/* ── Section 3: Melhores Práticas ── */}
          <section id="praticas" className="mb-16 fade-in-up">
            <div className="flex items-start gap-4 mb-6">
              <div className="w-12 h-12 bg-[#1C3B2D] rounded-lg flex items-center justify-center flex-shrink-0">
                <BookOpen className="w-6 h-6 text-[#C9A227]" />
              </div>
              <div>
                <span className="section-number">§3</span>
                <h2
                  className="text-2xl lg:text-3xl font-bold text-[#1C3B2D] mt-1"
                  style={{ fontFamily: "'Playfair Display', serif" }}
                >
                  Melhores Práticas
                </h2>
                <p className="text-[#4A4A4A] text-sm mt-1">
                  Guia prático baseado nas diretrizes da ANBIMA, CVM e especialistas em Direito Digital
                </p>
              </div>
            </div>

            <p className="text-[#4A4A4A] leading-relaxed mb-6">
              A ANBIMA monitora publicações sobre finanças e investimentos 24/7 com robôs e
              inteligência artificial, em convênio com a CVM desde 2021. Seguir as melhores
              práticas não é apenas uma questão legal — é o que diferencia um criador de
              conteúdo respeitável de um operador irregular.
            </p>

            <div className="space-y-1">
              {bestPractices.map((item, i) => (
                <AccordionCard key={i} item={item} index={i} />
              ))}
            </div>

            {/* ANBIMA Dicas */}
            <div className="mt-6 p-5 bg-white rounded-lg border border-[#D4CFC5] shadow-sm">
              <h3
                className="font-bold text-[#1C3B2D] mb-3 flex items-center gap-2"
                style={{ fontFamily: "'Playfair Display', serif" }}
              >
                <span className="text-[#C9A227]">✦</span>
                Regras de Bolso da ANBIMA para Finfluencers
              </h3>
              <p className="text-[#4A4A4A] text-sm mb-3">
                Nunca deixe de informar nos seus posts:
              </p>
              <div className="grid sm:grid-cols-2 gap-2">
                {[
                  "Se você tem registros na CVM ou certificações",
                  "Se você tem vínculo profissional com alguma instituição financeira",
                  "Se alguma instituição financeira patrocina seu conteúdo",
                  "Se os ativos que você está abordando fazem parte da sua carteira",
                  "Se há qualquer conflito de interesse no conteúdo",
                ].map((tip, i) => (
                  <div key={i} className="flex items-start gap-2 text-sm text-[#4A4A4A]">
                    <CheckCircle className="w-4 h-4 text-[#1A7A4A] flex-shrink-0 mt-0.5" />
                    <span>{tip}</span>
                  </div>
                ))}
              </div>
            </div>
          </section>

          {/* ── Section 4: Disclaimers ── */}
          <section id="disclaimers" className="mb-16 fade-in-up">
            <div className="flex items-start gap-4 mb-6">
              <div className="w-12 h-12 bg-[#1C3B2D] rounded-lg flex items-center justify-center flex-shrink-0">
                <FileText className="w-6 h-6 text-[#C9A227]" />
              </div>
              <div>
                <span className="section-number">§4</span>
                <h2
                  className="text-2xl lg:text-3xl font-bold text-[#1C3B2D] mt-1"
                  style={{ fontFamily: "'Playfair Display', serif" }}
                >
                  Disclaimers Prontos para Usar
                </h2>
                <p className="text-[#4A4A4A] text-sm mt-1">
                  Copie e cole diretamente nos seus posts
                </p>
              </div>
            </div>

            <div className="p-4 bg-[#FEF3CD] border border-[#C47A00]/30 rounded-lg mb-6">
              <div className="flex items-start gap-3">
                <AlertTriangle className="w-5 h-5 text-[#C47A00] flex-shrink-0 mt-0.5" />
                <p className="text-[#4A4A4A] text-sm leading-relaxed">
                  <strong>Importante:</strong> O disclaimer por si só não é suficiente para
                  descaracterizar uma recomendação se o conteúdo for habitual, remunerado e
                  apelativo. Ele é um elemento de boa-fé, não uma proteção absoluta. Use-o
                  sempre, mas em conjunto com as demais boas práticas.
                </p>
              </div>
            </div>

            <div className="space-y-4">
              {disclaimerTemplates.map((template, i) => (
                <DisclaimerCard key={i} template={template} />
              ))}
            </div>
          </section>

          {/* ── Section 5: Checklist ── */}
          <section id="checklist" className="mb-16 fade-in-up">
            <div className="flex items-start gap-4 mb-6">
              <div className="w-12 h-12 bg-[#1C3B2D] rounded-lg flex items-center justify-center flex-shrink-0">
                <Shield className="w-6 h-6 text-[#C9A227]" />
              </div>
              <div>
                <span className="section-number">§5</span>
                <h2
                  className="text-2xl lg:text-3xl font-bold text-[#1C3B2D] mt-1"
                  style={{ fontFamily: "'Playfair Display', serif" }}
                >
                  Checklist Antes de Publicar
                </h2>
                <p className="text-[#4A4A4A] text-sm mt-1">
                  Verifique cada item antes de postar seu diário de operações
                </p>
              </div>
            </div>

            {/* Progress */}
            <div className="bg-white rounded-lg border border-[#D4CFC5] p-5 mb-6 shadow-sm">
              <div className="flex items-center justify-between mb-3">
                <span className="text-sm font-semibold text-[#1C3B2D]">
                  Progresso do Checklist
                </span>
                <span className="text-sm font-bold text-[#1C3B2D]">
                  {checkedCount}/{checklistItems.length} itens
                </span>
              </div>
              <div className="w-full bg-[#EDE8DC] rounded-full h-3 overflow-hidden">
                <div
                  className="h-3 rounded-full transition-all duration-500"
                  style={{
                    width: `${progress}%`,
                    backgroundColor:
                      progress === 100
                        ? "#1A7A4A"
                        : progress >= 70
                        ? "#C9A227"
                        : "#B52B2B",
                  }}
                />
              </div>
              <div className="mt-2 text-xs text-[#4A4A4A]">
                {progress === 100
                  ? "✅ Post pronto para publicação!"
                  : progress >= 70
                  ? "⚠️ Quase lá — revise os itens restantes"
                  : "🔴 Revise os itens antes de publicar"}
              </div>
            </div>

            <div className="space-y-2">
              {checklistItems.map((item, i) => (
                <div
                  key={i}
                  className={`flex items-start gap-3 p-4 rounded-lg border cursor-pointer transition-all ${
                    checked[i]
                      ? "bg-[#E6F4ED] border-[#1A7A4A]/30"
                      : "bg-white border-[#D4CFC5] hover:border-[#1C3B2D]/30"
                  }`}
                  onClick={() => toggleCheck(i)}
                >
                  <div
                    className={`w-5 h-5 rounded border-2 flex-shrink-0 mt-0.5 flex items-center justify-center transition-all ${
                      checked[i]
                        ? "bg-[#1A7A4A] border-[#1A7A4A]"
                        : "border-[#D4CFC5]"
                    }`}
                  >
                    {checked[i] && (
                      <svg
                        className="w-3 h-3 text-white"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                        strokeWidth={3}
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          d="M5 13l4 4L19 7"
                        />
                      </svg>
                    )}
                  </div>
                  <div className="flex-1">
                    <p
                      className={`text-sm leading-relaxed ${
                        checked[i]
                          ? "text-[#1A7A4A] line-through"
                          : "text-[#1A1A1A]"
                      }`}
                    >
                      {item.text}
                    </p>
                    <span
                      className={`text-xs mt-1 inline-block px-2 py-0.5 rounded-full font-semibold ${
                        item.category === "cvm"
                          ? "bg-[#E8F0EB] text-[#1C3B2D]"
                          : item.category === "meta"
                          ? "bg-[#FEF3CD] text-[#C47A00]"
                          : "bg-[#F0EDE6] text-[#4A4A4A]"
                      }`}
                    >
                      {item.category === "cvm"
                        ? "CVM"
                        : item.category === "meta"
                        ? "Instagram/Meta"
                        : "Boa Prática"}
                    </span>
                  </div>
                </div>
              ))}
            </div>

            <div className="mt-6 p-4 bg-[#1C3B2D] text-white rounded-lg">
              <p className="text-sm leading-relaxed text-white/90">
                <strong className="text-[#C9A227]">Lembre-se:</strong> Este checklist é uma
                ferramenta de apoio baseada nas diretrizes públicas da CVM e da Meta. Não
                substitui aconselhamento jurídico profissional. Para situações específicas ou
                dúvidas sobre compliance, consulte um advogado especializado em Direito Digital
                e Mercado de Capitais.
              </p>
            </div>
          </section>

          {/* ── Sources ── */}
          <section className="fade-in-up">
            <div className="border-t border-[#D4CFC5] pt-8">
              <h3
                className="font-bold text-[#1C3B2D] mb-4"
                style={{ fontFamily: "'Playfair Display', serif" }}
              >
                Fontes e Referências
              </h3>
              <div className="grid sm:grid-cols-2 gap-3">
                {[
                  {
                    title: "Resolução CVM nº 20/2021",
                    desc: "Atividade de analista de valores mobiliários",
                    url: "https://www.gov.br/cvm/pt-br",
                  },
                  {
                    title: "ANBIMA — Espaço FInfluence",
                    desc: "Manual de melhores práticas para finfluencers",
                    url: "https://www.anbima.com.br/pt_br/especial/manual-melhores-praticas-finfluencers.htm",
                  },
                  {
                    title: "CVM — Agenda Regulatória 2026",
                    desc: "Regulamentação de finfluencers prevista",
                    url: "https://www.gov.br/cvm/pt-br/assuntos/noticias/2026",
                  },
                  {
                    title: "Meta — Padrões da Comunidade",
                    desc: "Políticas para conteúdo financeiro",
                    url: "https://transparency.meta.com/pt-br/policies/community-standards/",
                  },
                  {
                    title: "Portal do Investidor — CVM",
                    desc: "Diferença entre educação e atividade regulada",
                    url: "https://www.gov.br/investidor/pt-br",
                  },
                  {
                    title: "Consultor Jurídico — Dez/2025",
                    desc: "Influenciadores podem falar sobre investimentos?",
                    url: "https://www.conjur.com.br/2025-dez-08/influenciadores-digitais-podem-falar-sobre-investimentos-em-redes-sociais/",
                  },
                ].map(({ title, desc, url }) => (
                  <a
                    key={title}
                    href={url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-start gap-3 p-3 bg-white rounded-lg border border-[#D4CFC5] hover:border-[#1C3B2D] hover:shadow-sm transition-all group"
                  >
                    <ExternalLink className="w-4 h-4 text-[#C9A227] flex-shrink-0 mt-0.5 group-hover:text-[#1C3B2D] transition-colors" />
                    <div>
                      <p className="text-sm font-semibold text-[#1C3B2D]">{title}</p>
                      <p className="text-xs text-[#4A4A4A] mt-0.5">{desc}</p>
                    </div>
                  </a>
                ))}
              </div>
            </div>
          </section>
        </div>
      </div>

      {/* ── Footer ── */}
      <footer className="bg-[#1C3B2D] text-white mt-16 py-10">
        <div className="container">
          <div className="max-w-4xl mx-auto text-center">
            <Scale className="w-8 h-8 text-[#C9A227] mx-auto mb-4" />
            <h3
              className="text-xl font-bold mb-2"
              style={{ fontFamily: "'Playfair Display', serif" }}
            >
              Guia de Compliance para Criadores de Conteúdo Financeiro
            </h3>
            <p className="text-white/70 text-sm leading-relaxed max-w-xl mx-auto mb-6">
              Este guia foi elaborado com base em fontes públicas da CVM, ANBIMA e Meta. Não
              constitui aconselhamento jurídico. As regras estão sujeitas a mudanças — consulte
              sempre um profissional habilitado para situações específicas.
            </p>
            <div className="flex flex-wrap justify-center gap-4 text-xs text-white/50">
              <span>Baseado em: CVM • ANBIMA • Meta Transparency</span>
              <span>•</span>
              <span>Atualizado: Maio/2026</span>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
