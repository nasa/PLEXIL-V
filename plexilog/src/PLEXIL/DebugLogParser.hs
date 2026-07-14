module PLEXIL.DebugLogParser where

import PLEXIL.Trace
import qualified Data.Set as Set
import Text.Parsec hiding (State(..))
import Text.ParserCombinators.Parsec.Number (hexadecimal, nat)
import Text.Regex.Posix ((=~))
import Text.Parsec (ParseError)
import PLEXIL.Trace (Trace)

filterAndParseTrace :: String -> Either ParseError Trace
filterAndParseTrace = parseTrace . filterEntries

parseTrace :: String -> Either ParseError Trace
parseTrace = parse traceParser "trace"

traceParser :: Parsec String () Trace
traceParser = Trace <$> many (try macroParser) <* eof <?> "full trace"

parseMacro :: String -> Either ParseError Macro
parseMacro = parse macroParser "macro"

macroParser :: Parsec String () Macro
macroParser = do
  parseMacroStart
  ms <- many (try microParser)
  parseMacroEnd
  return $ Macro $ ms

parseMacroStart :: Parsec String () ()
parseMacroStart =
  choice [try $ string "[PlexilExec:cycle] ==>Start cycle ",string "[PlexilExec:step] ==>Start cycle "] *> nat *> spaceEOL *> pure ()

parseMacroEnd :: Parsec String () ()
parseMacroEnd =
  choice [try $ (string "[PlexilExec:cycle] ==>End cycle "),string "[PlexilExec:step] ==>End cycle "] *> nat *> ((try spaceEOL *> pure ()) <|> eof)

parseMicro :: String -> Either ParseError Micro
parseMicro = parse microParser "micro"

microParser :: Parsec String () Micro
microParser = do
  (trId,tr) <- transitionParserWithId []
  let uId = take 2 trId
  pairs <- many $ try $ transitionParserWithId uId
  let trs = map snd pairs
  return $ Micro $ Set.fromList (tr:trs)

parseTransition :: String -> Either ParseError Transition
parseTransition = parse transitionParser "transition"

transitionParser :: Parsec String () Transition
transitionParser = transitionParserWithId [] >>= \(id,t) -> return t

transitionParserWithId :: [Int] -> Parsec String () ([Int],Transition)
transitionParserWithId inputTransId = do
  spaces *> string "[PlexilExec:step]"
  trId <- case inputTransId of
            [] -> between (char '[') (char ']') $ nat `sepBy` char ':'
            [mId,uId] -> between (char '[') (char ']') $ do
              string $ show mId
              char ':'
              string $ show uId
              char ':'
              tId <- nat
              return [mId,uId,tId]
  spaces
  (try $ string "Transitioning node") <|> (string "Transitioning" *> spaces *> many1 letter *> spaces *> string "node")
  spaces
  id <- idParser
  spaces
  input <- getInput
  char '0' *> hexadecimal
  spaces
  string "from"
  spaces
  from <- stateParser
  spaces
  string "to"
  spaces
  to <- stateParser
  spaceEOL
  return $ (trId,Transition (Id id) from to)

stateParser :: Parsec String () State
stateParser =
  choice
    [ Inactive <$ ((try $ string "INACTIVE") <|> (try $ string "inactive")),
      Waiting <$ ((try $ string "WAITING") <|> (try $ string "waiting")),
      Failing <$ ((try $ string "FAILING") <|> (try $ string "failing")),
      Executing <$ ((try $ string "EXECUTING") <|> (try $ string "executing")),
      IterationEnded <$ ((try $ string "ITERATION_ENDED") <|> (try $ string "iterationEnded")),
      Finished <$ ((try $ string "FINISHED") <|> (try $ string "finished")),
      Finishing <$ ((try $ string "FINISHING") <|> (try $ string "finishing"))
    ]
    <?> "state"

idParser :: Parsec String () String
idParser = fmap maudifyLabel $ (:) <$> (letter <|> char '\'') <*> many (alphaNum <|> oneOf ['_', '-'] <?> "identifier")

maudifyLabel :: String -> String
maudifyLabel = ('\'' :)

spaceEOL :: Parsec String () Char
spaceEOL = optional (try nonEOLSpaces) *> endOfLine
  where nonEOLSpaces = skipMany nonEOLSpace
        nonEOLSpace = notFollowedBy endOfLine *> space

isKeyEntry :: String -> Bool
isKeyEntry s = foldl (\x y -> x || (s =~ y)) False ps
  where
    ps =
      [ "^\\[PlexilExec:step]\\[[0-9]+:[0-9]+:[0-9]+] Transitioning [ a-zA-Z]*node .+$",
        "^\\[PlexilExec:step] ==>Start cycle [0-9]+$",
        "^\\[PlexilExec:step] ==>End cycle [0-9]+$",
        "^\\[PlexilExec:cycle] ==>Start cycle [0-9]+$",
        "^\\[PlexilExec:cycle] ==>End cycle [0-9]+$"
      ]

filterEntries :: String -> String
filterEntries = unlines . filter isKeyEntry . lines