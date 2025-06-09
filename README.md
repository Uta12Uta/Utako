\section*{概要}
この課題では、Python を用いて電卓プログラムを段階的に拡張していった。それぞれの宿題で実装した機能は以下の通りである。

\begin{itemize}
  \item 宿題1：掛け算・割り算の優先順位対応
  \item 宿題2：テストケースを用いた検証
  \item 宿題3：括弧の優先順位対応
  \item 宿題4：abs, int, round の関数対応
\end{itemize}

\section*{宿題1：掛け算と割り算の優先順位}
\subsection*{目的}
\verb|+| や \verb|-| よりも \verb|*| や \verb|/| を先に計算する必要があるため、優先順位の制御を行う。

\subsection*{実装内容}
\verb|calculate_ordered1| 関数を定義し、トークン列から \texttt{MULTIPLY} または \texttt{DIVIDE} に対応する部分を先に計算する。


\section*{宿題2：テストと検証}
\subsection*{目的}
掛け算と割り算の優先順位が正しく実装されているかを確認するため、様々な入力例で検証する。

\subsection*{テスト例と意図}

\begin{tabular}{|c|c|l|}
\hline
入力 & 期待結果 & テストの意図 \\
\hline
\verb|2 + 3 * 4| & 14 & 掛け算の優先 \\
\verb|8 / 4 * 2| & 4  & 割り算と掛け算の左から処理 \\
\verb|(2 + 3) * 4| & 20 & 括弧の優先順位 \\
\verb|3.5 + 2 * 2| & 7.5 & 小数を含む演算 \\
\verb|10 / 0| & Error & ゼロ除算の例外処理 \\
\hline
\end{tabular}

\section*{宿題3：括弧の優先順位}
\subsection*{目的}
\verb|(3 + 4) * 2| のような括弧内の式を最優先で評価するために、括弧の処理を追加する。

\subsection*{実装内容}
\verb|calculate_ordered2| 関数を作成し、トークン列に \texttt{BRA}（開き括弧）と \texttt{KET}（閉じ括弧）があった場合に、その内部の式を再帰的に評価する。



\section*{宿題4：abs, int, round 関数の追加}
\subsection*{目的}
数学関数 \verb|abs|, \verb|int|, \verb|round| を扱えるようにして、より汎用的な電卓を実装する。

\subsection*{実装内容}
\begin{itemize}
  \item \verb|tokenize| 関数で文字列 \texttt{"abs"}, \texttt{"round"}, \texttt{"int"} を検出し、それぞれのトークンを作成。
  \item \verb|calculate_ordered2| 関数で、それらの関数の後に来る括弧内を評価して、関数を適用。
\end{itemize}



