import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { Toaster } from "@/components/ui/toaster";
import { TooltipProvider } from "@/components/ui/tooltip";
import AppLayout from "./components/layout/AppLayout";
import Dashboard from "./pages/Dashboard";
import Almacen from "./pages/Almacen";
import Productos from "./pages/Productos";
import Produccion from "./pages/Produccion";
import Ventas from "./pages/Ventas";
import Finanzas from "./pages/Finanzas";
import Configuracion from "./pages/Configuracion";
import Login from "./pages/Login";
import NotFound from "./pages/NotFound.tsx";

const queryClient = new QueryClient();

const App = () => (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      <Toaster />
      <Sonner />
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route element={<AppLayout />}>
            <Route path="/" element={<Dashboard />} />
            <Route path="/almacen" element={<Almacen />} />
            <Route path="/productos" element={<Productos />} />
            <Route path="/produccion" element={<Produccion />} />
            <Route path="/ventas" element={<Ventas />} />
            <Route path="/finanzas" element={<Finanzas />} />
            <Route path="/configuracion" element={<Configuracion />} />
          </Route>
          <Route path="*" element={<NotFound />} />
        </Routes>
      </BrowserRouter>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;
