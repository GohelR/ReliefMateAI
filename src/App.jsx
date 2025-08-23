import React from "react";
import { motion } from "framer-motion";
import {
  ArrowRight, MapPin, Shield, Languages, LifeBuoy, Github,
  MessageSquare, Activity, Globe2,
} from "lucide-react";

const fadeIn = { hidden: { opacity: 0, y: 24 }, show: { opacity: 1, y: 0, transition: { duration: 0.6 } } };
const stagger = { hidden: {}, show: { transition: { staggerChildren: 0.12 } } };

const FloatingOrb = ({ className = "" }) => (
  <motion.div initial={{ opacity: 0, scale: 0.6 }} animate={{ opacity: 0.7, scale: 1 }} transition={{ duration: 1.2 }}
    className={`pointer-events-none absolute rounded-full blur-2xl ${className}`} />
);

export default function App() {
  const links = {
  demo: "https://reliefmateai811.streamlit.app/",
  github: "https://github.com/GohelR/ReliefMateAI",
  email: "mailto:ravi.n.gohel811@gmail.com",
};

  return (
    <div className="min-h-screen w-full bg-slate-950 text-slate-100 overflow-x-hidden">
      {/* Background */}
      <div className="fixed inset-0 -z-10">
        <div className="absolute inset-0 bg-[radial-gradient(60%_60%_at_50%_0%,rgba(56,189,248,0.25),transparent_70%)]" />
        <div className="absolute inset-0 bg-[radial-gradient(60%_60%_at_0%_100%,rgba(16,185,129,0.18),transparent_70%)]" />
        <div className="absolute inset-0 bg-[radial-gradient(60%_60%_at_100%_100%,rgba(168,85,247,0.16),transparent_70%)]" />
        <FloatingOrb className="w-[40vw] h-[40vw] left-[-10vw] top-[-10vw] bg-cyan-500/20" />
        <FloatingOrb className="w-[30vw] h-[30vw] right-[-10vw] bottom-[-10vw] bg-emerald-500/20" />
      </div>

      {/* Navbar */}
      <header className="sticky top-0 z-40 backdrop-blur supports-[backdrop-filter]:bg-slate-950/40">
        <div className="mx-auto max-w-7xl px-4 py-3 flex items-center justify-between">
          <a href="#top" className="font-semibold tracking-tight text-lg">ReliefMate <span className="text-cyan-400">AI</span></a>
          <nav className="hidden md:flex gap-6 text-sm">
            <a href="#problem" className="hover:text-cyan-300">Problem</a>
            <a href="#solution" className="hover:text-cyan-300">Solution</a>
            <a href="#features" className="hover:text-cyan-300">Features</a>
            <a href="#how" className="hover:text-cyan-300">How it works</a>
            <a href="#demo" className="hover:text-cyan-300">Demo</a>
          </nav>
          <div className="flex gap-2">
            <a href={links.github} target="_blank" rel="noreferrer"
               className="px-3 py-2 rounded-xl bg-slate-800/60 hover:bg-slate-700 transition inline-flex items-center gap-2 text-sm">
              <Github className="w-4 h-4" /> GitHub
            </a>
            <a href={links.demo} target="_blank" rel="noreferrer"
               className="px-4 py-2 rounded-xl bg-cyan-500 hover:bg-cyan-400 text-slate-900 font-semibold inline-flex items-center gap-2 text-sm">
              Live Demo <ArrowRight className="w-4 h-4" />
            </a>
          </div>
        </div>
      </header>

      {/* Hero */}
      <section id="top" className="relative">
        <div className="mx-auto max-w-7xl px-4 py-20 md:py-28">
          <motion.div variants={stagger} initial="hidden" whileInView="show"
            viewport={{ once: true, amount: 0.3 }} className="grid md:grid-cols-2 gap-10 items-center">
            <motion.div variants={fadeIn}>
              <span className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-slate-800/70 text-xs border border-slate-700">
                <Activity className="w-3.5 h-3.5 text-emerald-300" /> Real‑time Relief Intelligence
              </span>
              <h1 className="mt-4 text-4xl md:text-6xl font-extrabold leading-tight">
                AI‑Powered Disaster Relief, <span className="block text-cyan-300">when every second counts.</span>
              </h1>
              <p className="mt-4 text-slate-300 max-w-xl">
                During floods, earthquakes and crises, ReliefMate AI delivers verified shelters, medical aid and helpline info in seconds — multilingual and accessible.
              </p>
              <div className="mt-6 flex flex-wrap gap-3">
                <a href={links.demo} target="_blank" rel="noreferrer"
                   className="px-5 py-3 rounded-2xl bg-cyan-500 hover:bg-cyan-400 text-slate-900 font-semibold inline-flex items-center gap-2">
                  Try Live Demo <ArrowRight className="w-5 h-5" />
                </a>
                <a href="#features"
                   className="px-5 py-3 rounded-2xl bg-slate-800/70 hover:bg-slate-700 font-semibold inline-flex items-center gap-2">
                  Explore Features
                </a>
              </div>
            </motion.div>

            <motion.div variants={fadeIn} className="relative">
              {/* Animated card stack */}
              <motion.div initial={{ rotate: -6, y: 10 }} animate={{ rotate: -4, y: 0 }} transition={{ duration: 1.2 }}
                className="absolute -top-4 -left-6 w-64 h-40 rounded-2xl bg-slate-900/80 border border-slate-700 p-4 shadow-xl">
                <div className="text-xs text-slate-400">Incoming request</div>
                <div className="mt-2 text-sm">“Need medical help in Rajkot, insulin for 2 patients.”</div>
                <div className="mt-4 inline-flex items-center gap-2 text-emerald-300 text-xs">
                  <Shield className="w-4 h-4"/> Classified: Medical</div>
              </motion.div>
              <motion.div initial={{ rotate: 5, y: 20 }} animate={{ rotate: 3, y: 6 }}
                transition={{ duration: 1.2, delay: 0.1 }}
                className="absolute top-24 -right-6 w-64 h-40 rounded-2xl bg-slate-900/80 border border-slate-700 p-4 shadow-xl">
                <div className="text-xs text-slate-400">Shelter locator</div>
                <div className="mt-2 text-sm inline-flex items-center gap-2">
                  <MapPin className="w-4 h-4 text-cyan-300"/> Nearest relief camp: 2.1 km</div>
                <div className="mt-2 text-xs text-slate-400">Open · Verified 10m ago</div>
              </motion.div>
              <motion.div initial={{ scale: 0.9, opacity: 0 }} animate={{ scale: 1, opacity: 1 }}
                transition={{ duration: 0.9, delay: 0.15 }}
                className="relative z-10 w-full rounded-3xl bg-gradient-to-br from-slate-900 to-slate-800 border border-slate-700 p-6 shadow-2xl">
                <div className="text-sm text-slate-300">ReliefMate Chat</div>
                <div className="mt-3 rounded-xl bg-slate-900/80 border border-slate-700 p-3 text-sm">
                  <div className="text-slate-400">You</div>
                  <div>Nearest shelter in my area?</div>
                </div>
                <div className="mt-3 rounded-xl bg-slate-900/80 border border-slate-700 p-3 text-sm">
                  <div className="text-cyan-300">ReliefMate</div>
                  <div>Verified shelter at Govt School, Ward 4. Capacity 120. Open now. Helpline: 108.</div>
                </div>
              </motion.div>
            </motion.div>
          </motion.div>
        </div>
      </section>

      {/* Problem */}
      <section id="problem" className="border-t border-slate-800/60">
        <div className="mx-auto max-w-7xl px-4 py-16">
          <motion.div variants={fadeIn} initial="hidden" whileInView="show" viewport={{ once: true, amount: 0.3 }}
            className="grid md:grid-cols-3 gap-8">
            <div className="md:col-span-1">
              <h2 className="text-2xl md:text-3xl font-bold">The Challenge</h2>
              <p className="mt-3 text-slate-300">Disaster info is scattered and slow. Misinformation and language gaps cost lives.</p>
            </div>
            <ul className="md:col-span-2 grid gap-4">
              {[
                "Victims lack verified shelter & medical info when it matters most.",
                "Relief efforts are fragmented across channels and languages.",
                "Volunteers have no single source of truth or prioritization.",
              ].map((t, i) => (
                <motion.li key={i} initial={{ opacity: 0, x: 20 }} whileInView={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.4, delay: i * 0.08 }}
                  className="rounded-2xl bg-slate-900/60 border border-slate-800 p-4">
                  {t}
                </motion.li>
              ))}
            </ul>
          </motion.div>
        </div>
      </section>

      {/* Solution */}
      <section id="solution" className="border-t border-slate-800/60">
        <div className="mx-auto max-w-7xl px-4 py-16">
          <motion.h2 variants={fadeIn} initial="hidden" whileInView="show" viewport={{ once: true, amount: 0.3 }}
            className="text-2xl md:text-3xl font-bold">Our Solution</motion.h2>
          <p className="mt-3 text-slate-300 max-w-3xl">ReliefMate AI delivers verified relief information through an AI assistant with multilingual support and a forthcoming NGO dashboard for triage and coordination.</p>

          <motion.div variants={stagger} initial="hidden" whileInView="show" viewport={{ once: true, amount: 0.3 }}
            className="mt-8 grid sm:grid-cols-2 lg:grid-cols-4 gap-5">
            {[
              { icon: MessageSquare, title: "Chatbot 24/7", desc: "Instant guidance for shelters, helplines and hospitals." },
              { icon: Shield, title: "Verified Updates", desc: "Summarized, trustworthy information from official sources." },
              { icon: Languages, title: "Multilingual", desc: "Answers in regional languages to remove barriers." },
              { icon: LifeBuoy, title: "Request Types", desc: "Rescue, Medical, Food, Shelter — auto‑categorized." },
            ].map(({ icon: Icon, title, desc }, i) => (
              <motion.div key={i} variants={fadeIn} className="rounded-2xl h-full bg-slate-900/60 border border-slate-800 p-5">
                <div className="w-10 h-10 rounded-xl bg-cyan-500/10 border border-cyan-500/30 flex items-center justify-center">
                  <Icon className="w-5 h-5 text-cyan-300" />
                </div>
                <h3 className="mt-4 font-semibold text-lg">{title}</h3>
                <p className="mt-1 text-sm text-slate-300">{desc}</p>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* How it works */}
      <section id="how" className="border-t border-slate-800/60">
        <div className="mx-auto max-w-7xl px-4 py-16">
          <motion.h2 variants={fadeIn} initial="hidden" whileInView="show" viewport={{ once: true, amount: 0.3 }}
            className="text-2xl md:text-3xl font-bold">How It Works</motion.h2>
          <div className="mt-8 grid md:grid-cols-3 gap-6">
            {[
              { step: "1", title: "Ask for help", desc: "Web or mobile chatbot collects free‑text requests.", icon: MessageSquare },
              { step: "2", title: "AI understands", desc: "Classifies need, fetches verified resources and translates.", icon: Globe2 },
              { step: "3", title: "Rapid response", desc: "Clear guidance delivered instantly. Dashboard triage coming soon.", icon: Activity },
            ].map(({ step, title, desc, icon: Icon }, i) => (
              <motion.div key={i} initial={{ opacity: 0, y: 16 }} whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: i * 0.08 }}
                className="relative rounded-2xl bg-slate-900/60 border border-slate-800 p-6">
                <div className="absolute -top-3 -left-3 w-10 h-10 rounded-xl bg-cyan-500 text-slate-900 font-bold flex items-center justify-center shadow-lg">{step}</div>
                <div className="ml-6"><Icon className="w-6 h-6 text-cyan-300" /></div>
                <h3 className="mt-2 font-semibold text-lg">{title}</h3>
                <p className="mt-1 text-sm text-slate-300">{desc}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Demo */}
      <section id="demo" className="border-t border-slate-800/60">
        <div className="mx-auto max-w-7xl px-4 py-16 text-center">
          <motion.h2 variants={fadeIn} initial="hidden" whileInView="show" viewport={{ once: true, amount: 0.3 }}
            className="text-2xl md:text-3xl font-bold">Try the Live Demo</motion.h2>
          <p className="mt-3 text-slate-300 max-w-2xl mx-auto">
            Experience ReliefMate AI in action. Ask about shelters, helplines or submit a need.
          </p>
          <div className="mt-6 flex gap-3 justify-center">
            <a href={links.demo} target="_blank" rel="noreferrer"
               className="px-6 py-3 rounded-2xl bg-cyan-500 hover:bg-cyan-400 text-slate-900 font-semibold inline-flex items-center gap-2">
              Open Live Demo <ArrowRight className="w-5 h-5" />
            </a>
            <a href={links.github} target="_blank" rel="noreferrer"
               className="px-6 py-3 rounded-2xl bg-slate-800/70 hover:bg-slate-700 font-semibold inline-flex items-center gap-2">
              <Github className="w-5 h-5" /> View on GitHub
            </a>
          </div>
          <div className="mt-8 text-sm text-slate-400">
            Contact: <a className="underline hover:text-cyan-300" href="mailto:ravigohel226020332021@gmail.com">
              ravigohel226020332021@gmail.com</a>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-slate-800/60">
        <div className="mx-auto max-w-7xl px-4 py-10 flex flex-col md:flex-row items-center justify-between gap-4 text-sm text-slate-400">
          <div>© {new Date().getFullYear()} ReliefMate AI • Built by Ravi Gohel</div>
          <div className="flex items-center gap-6">
            <a className="hover:text-cyan-300" href={links.github} target="_blank" rel="noreferrer">GitHub</a>
            <a className="hover:text-cyan-300" href={links.demo} target="_blank" rel="noreferrer">Live Demo</a>
            <a className="hover:text-cyan-300" href={links.email}>Email</a>
          </div>
        </div>
      </footer>
    </div>
  );
}
