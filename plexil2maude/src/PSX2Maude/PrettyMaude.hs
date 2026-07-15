{-# LANGUAGE NamedFieldPuns #-}
{-# LANGUAGE ScopedTypeVariables #-}

module PSX2Maude.PrettyMaude where

import PLEXILScript

import Data.List (intersperse)
import Data.OneOfN (OneOf3(..), OneOf7(..))
import Prelude hiding ((<>))
import Debug.Trace
import Data.Typeable(typeOf)
import Text.PrettyPrint
import Data.Char (toLower)

class Pretty a where
  pretty :: a -> Doc

newtype PLEXILScript2Maude = ToMaude { unToMaude :: PLEXILScript } deriving (Show,Eq)

instance Pretty PLEXILScript2Maude where
  pretty (ToMaude (PLEXILScript { initialState, script })) =
    vcat $
      [text "mod INPUT is"
      ,nest 2 $ vcat $
        [text "protecting PLEXIL-V ."
        ,empty
        ,text "op input : -> InputGenerator ."
        ,text "eq input = sequenceGenerator("
        ,nest 2 $ vcat
          [pretty initialState
          ,text "#"
          ,pretty script]
        ,text ") ."
        ]
      ,text "endm"
      ]

instance Pretty InitialState where
  pretty (InitialState []) = text "noInputs"
  pretty (InitialState xs) = vcat (map pretty xs)

instance Pretty Script where
  pretty (Script []) = text "nilEInputsList"
  pretty (Script xs) = vcat $ intersperse (char '#') $ map pretty xs

instance Pretty ScriptEntry where
  pretty (ScriptEntry e)
    | (OneOf7 st)    <- e = pretty st
    | (TwoOf7 cmd)   <- e = pretty cmd
    | (ThreeOf7 ca)  <- e = pretty ca
    | (FourOf7 sim)  <- e = pretty sim
    | (FiveOf7 ua)   <- e = pretty ua
    | (SixOf7 cab)   <- e = pretty cab
    | (SevenOf7 del) <- e = pretty del

instance Pretty Delay where
  pretty _ = text "noInputs"

instance Pretty State where
  pretty State { stName, stParams, stValue, stType } =
    text "stateLookup"
      <> parens (
        hcat $ punctuate comma
          [ text "'" <> text stName
          , prettyParams stParams
          , case stType of
              PXBoolArray   -> arrayValues
              PXIntArray    -> arrayValues
              PXRealArray   -> arrayValues
              PXStringArray -> arrayValues
              PXString      -> stringValues
              _             -> otherValues
          ]
      )
    where
      arrayValues = text "array" <> parens (hcat $ punctuate (text " # ") $ map wrapValOrUnknown $ map unValue stValue)
      otherValues = case unValue $ head stValue of
        "Plexil_Unknown" -> text "unknown"
        val -> text "val" <> parens (text val)
      stringValues = case unValue $ head stValue of
        "Plexil_Unknown" -> text "unknown"
        val -> text "val" <> parens (doubleQuotes $ text val)
      prettyParams params = case params of
        [] -> text "nilarg"
        _  -> prettyList params
      prettyList params = parens $ hsep $ map (pretty) params
      wrapValOrUnknown str = case str of
        "Plexil_Unknown" -> text "unknown"
        _ -> wrapVal (text str)



wrapVal :: Doc -> Doc -- wraps document in "val(...)"
wrapVal doc = text "val" <> parens doc

instance Pretty Command where
  pretty (Command
    { cmdName
    , cmdParams
    , cmdResult
    , cmdType
    }) =
      text "commandResult"
        <> parens (
          hcat $ punctuate comma
            [text "'" <> text cmdName
            ,if null cmdParams then text "nilarg" else parens (hsep (map pretty cmdParams))
            ,pretty cmdResult]
        )

instance Pretty CommandAck where
  pretty (CommandAck
    { caName
    , caParams
    , caHandle
    , caType
    }) =
      text "commandAck"
        <> parens (
          hcat $ punctuate comma
            [text "'" <> text caName
            ,if null caParams then text "nilarg" else parens (hsep (map pretty caParams))
            ,pretty caHandle]
        )

instance Pretty CommandAbort where
  pretty (CommandAbort
    { cabName
    , cabParams
    , cabResult
    , cabType
    }) =
      text "commandAbort"
        <> parens (
          hcat $ punctuate comma
            [text "'" <> text cabName
            ,if null cabParams then text "nilarg" else parens (hsep (map pretty cabParams))
            , pretty cabResult]
        )

instance Pretty Parameter where
  pretty Parameter{ parValue, parType } =
    case parValue of
      "UNKNOWN" -> text "unknown"
      _ ->  case parType of
              PXReal -> prettyReal parValue
              PXInt  -> prettyValue parValue
              PXString -> prettyString parValue
              PXBool -> prettyBool parValue
              -- PXBoolArray -> prettyBoolArray parValue
              _ -> error $ "unimplemented pretty for parameters of type " ++ show parType
            where
              prettyReal valueStr =
                if isNumberWithDot valueStr
                  then prettyValue valueStr
                  else prettyValueWithCast "float" valueStr
                  where
                    isNumberWithDot :: String -> Bool
                    isNumberWithDot valueStr =
                      case reads valueStr of
                        [(v :: Double,"")] -> '.' `elem` valueStr
                        _                  -> error $ "Cannot parse as number: " ++ show valueStr

              prettyBool valueStr =
                text "val" <> parens (text $ case valueStr of
                                        "1" -> "true"
                                        "0" -> "false"
                                        "true"  -> "true"
                                        "false" -> "false"
                                      )

              prettyString valueStr =
                text "val" <> (parens . doubleQuotes) (text parValue)

              prettyValue valueStr =
                text "val" <> parens (text parValue)

              prettyValueWithCast typeStr valueStr =
                text "val" <> parens (text typeStr <> parens (text parValue))

              -- prettyBoolArray valueStrs =
              --   text "array" <> parens (hcat $ punctuate (text " # ") $ map prettyBool valueStrs)


instance Pretty Simultaneous where
  pretty (Simultaneous es) = vcat $ map pretty es

instance Pretty SimultaneousEntry where
  pretty (SimultaneousEntry e)
    | OneState       st <- e = pretty st
    | OneCommandAck ca <- e = pretty ca
    | OneCommandAbort cab <- e = pretty cab
    | OneCommand cmd      <- e = pretty cmd

instance Pretty CommandHandle where
  pretty CommandDenied = text "CommandDenied"
  pretty CommandAccepted = text "CommandAccepted"
  pretty CommandSentToSystem = text "CommandSentToSystem"
  pretty CommandReceivedBySystem = text "CommandReceivedBySystem"
  pretty CommandSuccess = text "CommandSuccess"
  pretty CommandFailed = text "CommandFailed"
  pretty CommandInterfaceError = text "CommandInterfaceError"

instance Pretty Value where
  pretty (Value str) =
    case str of
      "Plexil_Unknown" -> text "unknown"
      _ -> text str
  pretty (TypedValue (TVBoolArray bs)) = text "array" <> parens values
    where
      values = hcat $ punctuate (text " # ") $
        map
          (\b -> if b
            then text "val(true)"
            else text "val(false)")
          bs
  pretty (TypedValue (TVStringArray ss)) = text "array" <> parens values
    where
      values = hcat $ punctuate (text " # ") $
        map
          (\s -> case s of
                   "Plexil_Unknown" -> text "unknown"
                   _ -> text "val" <> parens (doubleQuotes $ text s))
          ss
  pretty (TypedValue (TVIntArray is)) = text "array" <> parens values
    where
      values = hcat $ punctuate (text " # ") $
        map
          (\i -> text "val" <> parens (text $ show i))
          is
  pretty (TypedValue (TVRealArray rs)) = text "array" <> parens values
    where
      values = hcat $ punctuate (text " # ") $
        map
          (\r -> text "val" <> parens (text $ show r))
          rs
  pretty (TypedValue (TVBool b)) = text "val" <> parens (text $ if b then "true" else "false")
  pretty (TypedValue (TVString s)) =
    case s of
      "Plexil_Unknown" -> text "unknown"
      _ -> text "val" <> parens (doubleQuotes $ text s)
  pretty (TypedValue (TVInt i)) = text "val" <> parens (text $ show i)
  pretty (TypedValue (TVReal r)) = text "val" <> parens (text $ show r)
  pretty x = error $ "unimplemented pretty for value " ++ show x

instance Pretty Result where
  pretty = pretty . unResult

instance Pretty UpdateAck where
  pretty (UpdateAck
    { uaName
    , uaBool
    }) =
      text "updateAck"
        <> parens ( hcat $ punctuate comma
        [text "'" <> text uaName
        , text $ map toLower $ show uaBool]
        )