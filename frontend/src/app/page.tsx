import StocksCard from "../components/StocksCard";
import AppMenu from "../components/AppMenu";

export default function Home() {
  return (
    <div className="min-h-screen p-4">
      <AppMenu />
      <StocksCard />
    </div>
  );
}
