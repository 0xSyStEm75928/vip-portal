# jq用 ストリーム計算・インデックス付与スクリプト
map(path(..) as $p | select(getpath($p) | type != "object" and type != "array") | {
  index: $p,
  value: getpath($p)
})
