export default function Spinner({ size = 16 }) {
  return (
    <span
      className="inline-block rounded-full animate-spin border-2 border-[#1e2a45] border-t-blue-400"
      style={{ width: size, height: size }}
    />
  )
}
