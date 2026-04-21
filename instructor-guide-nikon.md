# 📋 講師向け：Organization 設定ガイド

企業の Organization でこのワークショップを実施する場合、以下の設定が必要です。

## 1. Codespaces の有効化

**設定場所**: Organization Settings → Code, planning, and automation → Codespaces

- **Enable for**: `All members` を選択
- **Ownership**: `Organization ownership` を選択

> ⚠️ Codespaces が無効の場合、参加者が Codespaces を起動できません。

### 💰 Codespaces の料金について

Codespaces の料金は **$0.18/hour**（2-core マシン）です。

| 項目 | 値 |
|---|---|
| 参加者数 | 300名 |
| ワークショップ時間 | 3時間 |
| 単価 | $0.18/hour |
| **合計概算** | **$162.00** |

> 📊 詳細な料金シミュレーションは [GitHub Pricing Calculator](https://github.com/pricing/calculator) をご利用ください。
>
> 💡 **ヒント**: Codespaces はアイドル状態で自動停止するため、実際の料金は上記より低くなる場合があります。Organization Settings で **idle timeout**（デフォルト30分）を設定し、コストを最適化できます。
