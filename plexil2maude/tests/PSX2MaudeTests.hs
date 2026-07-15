{-# LANGUAGE FlexibleInstances #-}
{-# LANGUAGE OverloadedStrings #-}
{-# LANGUAGE QuasiQuotes #-}
{-# LANGUAGE ScopedTypeVariables #-}

module PSX2MaudeTests where

import Control.Monad.Except
import Data.Either
import Prelude hiding ((<>))

import Test.Tasty
import Test.Tasty.HUnit
import Text.RawString.QQ
import Text.PrettyPrint (text)

import Text.XML.HXT.Core

import PLEXILScript
import PSX2Maude.PrettyMaude
import Text.PrettyPrint

import Data.OneOfN (OneOf7(..))


testPSX2Maude :: TestTree
testPSX2Maude =
  testGroup "PSX2Maude tests"
    [ testCommand
    , testCommandAck
    , testCommandAbort
    , testParameter
    , testValue
    , testSimultaneous
    , testCommandHandles
    , testUpdateAck
    , testScript
    , testPrettyPrint
    , testOptionalElements
    , testState
    , testDelay
    ]

testOptionalElements :: TestTree
testOptionalElements = testGroup "Optional XML Elements"
  [ testGroup "InitialState"
    [ [r||] `testItParsesAs` InitialState []
    ]
  ]
  where
    testItParsesAs :: String -> InitialState -> TestTree
    testItParsesAs str st = testCase (show st) $ str `parsesOnlyAs` st

testPrettyPrint :: TestTree
testPrettyPrint = testGroup "Pretty Printer"
  [ testGroup "Parameter"
    [ Parameter "10" PXReal `testPrettiesAs` "val(float(10))"
    , Parameter "10.0" PXReal `testPrettiesAs` "val(10.0)"
    , Parameter "11" PXInt  `testPrettiesAs` "val(11)"
    , Parameter "Valencia" PXString `testPrettiesAs` "val(\"Valencia\")"
    , Parameter "1" PXBool `testPrettiesAs` "val(true)"
    , Parameter "true" PXBool `testPrettiesAs` "val(true)"
    , Parameter "false" PXBool `testPrettiesAs` "val(false)"
    , Parameter "UNKNOWN" PXBool `testPrettiesAs` "unknown"
    , Parameter "UNKNOWN" PXReal `testPrettiesAs` "unknown"
    , Parameter "UNKNOWN" PXBoolArray `testPrettiesAs` "unknown"
    , Parameter "UNKNOWN" PXRealArray `testPrettiesAs` "unknown"
    -- , Parameter "0 0 1" PXBoolArray `testPrettiesAs` "array(val(False) # val(False) # val(True))"
    ]
  , testGroup "CommandAck"
    [ CommandAck "c1" [Parameter "1" PXInt] CommandAccepted PXString
        `testPrettiesAs`
           "commandAck('c1,(val(1)),CommandAccepted)"
    , CommandAck "c2" [Parameter "1" PXReal ,Parameter "10" PXInt] CommandDenied PXInt
        `testPrettiesAs`
           "commandAck('c2,(val(float(1)) val(10)),CommandDenied)"
    ]
  , testGroup "CommandAbort"
    [ CommandAbort "c1" [] (Result $ TypedValue (TVBool True)) PXBool
        `testPrettiesAs`
           "commandAbort('c1,nilarg,val(true))"
    , CommandAbort "c2" [] (Result $ TypedValue (TVBool False)) PXBool
        `testPrettiesAs`
           "commandAbort('c2,nilarg,val(false))"
    ]
  , testGroup "Command"
    [ Command "c1" [] (Result $ TypedValue (TVInt 1)) PXInt
        `testPrettiesAs`
           "commandResult('c1,nilarg,val(1))"
    , Command "c2" [] (Result $ TypedValue (TVBool True)) PXBool
        `testPrettiesAs`
           "commandResult('c2,nilarg,val(true))"
    , Command "c3" [] (Result $ TypedValue (TVString "Valencia")) PXString
        `testPrettiesAs`
           "commandResult('c3,nilarg,val(\"Valencia\"))"
    , Command "c4" [] (Result $ TypedValue (TVReal 1.1)) PXReal
        `testPrettiesAs`
           "commandResult('c4,nilarg,val(1.1))"
    , Command "c5" [] (Result $ TypedValue (TVString "Plexil_Unknown")) PXString
        `testPrettiesAs`
           "commandResult('c5,nilarg,unknown)"
    , Command "ac1" [] (Result $ TypedValue (TVIntArray [1,2,3])) PXIntArray
        `testPrettiesAs`
           "commandResult('ac1,nilarg,array(val(1) # val(2) # val(3)))"
    , Command "ac2" [] (Result $ TypedValue (TVBoolArray [True,False,True])) PXBoolArray
        `testPrettiesAs`
           "commandResult('ac2,nilarg,array(val(true) # val(false) # val(true)))"
    , Command "ac3" [] (Result $ TypedValue (TVStringArray ["Valencia","Y nadie","Más"])) PXStringArray
        `testPrettiesAs`
           "commandResult('ac3,nilarg,array(val(\"Valencia\") # val(\"Y nadie\") # val(\"Más\")))"
    , Command "ac4" [] (Result $ TypedValue (TVRealArray [1.1,2.2,3.3])) PXRealArray
        `testPrettiesAs`
           "commandResult('ac4,nilarg,array(val(1.1) # val(2.2) # val(3.3)))"
    , Command "ac5" [] (Result $ TypedValue (TVStringArray ["Plexil_Unknown","normal","Plexil_Unknown"])) PXStringArray
        `testPrettiesAs`
           "commandResult('ac5,nilarg,array(unknown # val(\"normal\") # unknown))"
    ]
  , testGroup "UpdateAck"
    [ UpdateAck "u1" True
        `testPrettiesAs`
           "updateAck('u1,true)"
    ]
  , testGroup "Emptyness of Script or Initial State"
    [ Script [] `testPrettiesAs` "nilEInputsList"
    , InitialState [] `testPrettiesAs` "noInputs"
    ]
  ]
  where
    testPrettiesAs :: forall a. (Pretty a,Show a) => a -> String -> TestTree
    testPrettiesAs p str =
      testCase (show p) $
        assertEqual "is not pretty printed as"
          (text str)
          (pretty p)


testCommand :: TestTree
testCommand = testGroup "Command"
  [ testGroup "from XML"
    [ [r|<Command name="get_bool" type="bool"><Result>1</Result></Command>|]
        `testItParsesAs`
          Command { cmdName = "get_bool"
                  , cmdParams = []
                  , cmdResult = Result $ TypedValue (TVBool True)
                  , cmdType = PXBool
                  }
    , [r|
<Command name="get_string" type="string">
  <Result></Result>
</Command>|]
        `testItParsesAs`
          Command { cmdName = "get_string"
                  , cmdParams = []
                  , cmdResult = Result $ TypedValue (TVString "")
                  , cmdType = PXString
                  }
    , "<Command name=\"get_string\" type=\"string\"><Result> \t\n</Result></Command>"
        `testItParsesAs`
          Command { cmdName = "get_string"
                  , cmdParams = []
                  , cmdResult = Result $ TypedValue (TVString " \t\n")
                  , cmdType = PXString
                  }
    , [r|
<Command name="get_string" type="string">
<Result> \n</Result>
</Command>|]
        `testItParsesAs`
          Command { cmdName = "get_string"
                  , cmdParams = []
                  , cmdResult = Result $ TypedValue (TVString " \n")
                  , cmdType = PXString
                  }
    , [r|<Command name="get_string" type="string"><Result>fred</Result></Command>|]
        `testItParsesAs`
          Command { cmdName = "get_string"
                  , cmdParams = []
                  , cmdResult = Result $ TypedValue (TVString "fred")
                  , cmdType = PXString
                  }
    , [r|<Command name="get_int" type="int"><Result>0</Result></Command>|]
        `testItParsesAs`
          Command { cmdName = "get_int"
                  , cmdParams = []
                  , cmdResult = Result $ TypedValue (TVInt 0)
                  , cmdType = PXInt
                  }
    , [r|<Command name="get_real" type="real"><Result>12.345</Result></Command>|]
        `testItParsesAs`
          Command { cmdName = "get_real"
                  , cmdParams = []
                  , cmdResult = Result $ TypedValue (TVReal 12.345)
                  , cmdType = PXReal
                  }
    , [r|<Command name="boolArrayCommand" type="bool-array"><Result>1</Result><Result>1</Result><Result>1</Result></Command>|]
        `testItParsesAs`
          Command { cmdName = "boolArrayCommand"
                  , cmdParams = []
                  , cmdResult = Result $ TypedValue (TVBoolArray [True,True,True])
                  , cmdType = PXBoolArray
                  }
    , [r|<Command name="get_string_aray" type="string-array"><Result>john</Result><Result>paul</Result><Result>george</Result><Result>ringo</Result></Command>|]
        `testItParsesAs`
          Command { cmdName = "get_string_aray"
                  , cmdParams = []
                  , cmdResult = Result $ TypedValue (TVStringArray ["john","paul","george","ringo"])
                  , cmdType = PXStringArray
                  }
    , [r|<Command name="get_int_aray" type="int-array"><Result>1</Result><Result>2</Result><Result>3</Result></Command>|]
        `testItParsesAs`
          Command { cmdName = "get_int_aray"
                  , cmdParams = []
                  , cmdResult = Result $ TypedValue (TVIntArray [1,2,3])
                  , cmdType = PXIntArray
                  }
    , [r|<Command name="get_real_aray" type="real-array"><Result>1.1</Result><Result>2.2</Result><Result>3.3</Result></Command>|]
        `testItParsesAs`
          Command { cmdName = "get_real_aray"
                  , cmdParams = []
                  , cmdResult = Result $ TypedValue (TVRealArray [1.1,2.2,3.3])
                  , cmdType = PXRealArray
                  }
    , [r|<Command name="get_real" type="real"><Param type="string">param</Param><Result>1.1</Result></Command>|]
        `testItParsesAs`
          Command { cmdName = "get_real"
                  , cmdParams = [
                      Parameter { parValue = "param"
                                , parType  = PXString
                                }
                  ]
                  , cmdResult = Result $ TypedValue (TVReal 1.1)
                  , cmdType = PXReal
                  }
    ]
  ]
  where
    testItParsesAs :: String -> Command -> TestTree
    testItParsesAs str cmd = testCase (show cmd) $ str `parsesOnlyAs` cmd

    testItPicklesAs :: Command -> String -> TestTree
    testItPicklesAs cmd str = testCase (show cmd) $ cmd `isPickledAs` str

testCommandAck :: TestTree
testCommandAck = testGroup "CommandAck"
  [ testGroup "fromXML"
    [
      [r|<CommandAck name="foo" type="string"><Param type="string">fred</Param><Result>COMMAND_SUCCESS</Result></CommandAck>|]
        `testItParsesAs`
          CommandAck { caName = "foo"
                    , caParams = [ Parameter { parValue = "fred"
                                              , parType  = PXString
                                              }
                                  ]
                    , caHandle = CommandSuccess
                    , caType = PXString
                    }
    ]
  ]
  where
    testItParsesAs :: String -> CommandAck -> TestTree
    testItParsesAs str cmd = testCase (show cmd) $ str `parsesOnlyAs` cmd

    testItPicklesAs :: CommandAck -> String -> TestTree
    testItPicklesAs cmd str = testCase (show cmd) $ cmd `isPickledAs` str

testCommandAbort :: TestTree
testCommandAbort = testGroup "CommandAbort"
  [ testGroup "fromXML"
    [
      [r|<CommandAbort name="ReceiveMessage" type="bool"><Param type="string">Foo</Param><Result>1</Result></CommandAbort>|]
        `testItParsesAs`
          CommandAbort { cabName = "ReceiveMessage"
                       , cabParams = [ Parameter { parValue = "Foo"
                                                 , parType  = PXString
                                                 }
                                     ]
                       , cabResult = Result $ TypedValue (TVBool True)
                       , cabType = PXBool
                       }
    , [r|<CommandAbort name="move_to_waypoint" type="int"><Param type="string">UNKNOWN</Param><Param type="real">4.0</Param><Param type="real">UNKNOWN</Param><Result>1</Result></CommandAbort>|]
        `testItParsesAs`
          CommandAbort { cabName = "move_to_waypoint"
                       , cabParams = [ Parameter { parValue = "UNKNOWN"
                                                 , parType  = PXString
                                                 }
                                     , Parameter { parValue = "4.0"
                                                 , parType  = PXReal
                                                 }
                                     , Parameter { parValue = "UNKNOWN"
                                                 , parType  = PXReal
                                                 }
                                     ]
                       , cabResult = Result $ TypedValue (TVInt 1)
                       , cabType = PXInt
                       }
    ]
  ]
  where
    testItParsesAs :: String -> CommandAbort -> TestTree
    testItParsesAs str cmd = testCase (show cmd) $ str `parsesOnlyAs` cmd

    testItPicklesAs :: CommandAbort -> String -> TestTree
    testItPicklesAs cmd str = testCase (show cmd) $ cmd `isPickledAs` str

testParameter :: TestTree
testParameter = testGroup "Parameter"
  [ testGroup "fromXML"
    [
      [r|<Param type="string">fred</Param>|]
        `testItParsesAs`
          Parameter { parValue = "fred"
                    , parType  = PXString
                    }
    , [r|<Param type="string"></Param>|]
        `testItParsesAs`
          Parameter { parValue = ""
                    , parType  = PXString
                    }
    ]
  ]
  where
    testItParsesAs :: String -> Parameter -> TestTree
    testItParsesAs str cmd = testCase (show cmd) $ str `parsesOnlyAs` cmd

    testItPicklesAs :: Parameter -> String -> TestTree
    testItPicklesAs cmd str = testCase (show cmd) $ cmd `isPickledAs` str

testValue :: TestTree
testValue = testGroup "Value"
  [ testGroup "fromXML"
    [
      [r|<Value>UNKNOWN</Value>|]
        `testItParsesAs`
          Value { unValue = "UNKNOWN" }
    , [r|<Value>Plexil_Unknown</Value>|]
        `testItParsesAs`
          Value { unValue = "Plexil_Unknown" }
    ]
  , testGroup "Pretty printing"
    [
      Value { unValue = "Plexil_Unknown" }
        `testValuePrettiesAs`
          "unknown"
    , TypedValue (TVString "Plexil_Unknown")
        `testValuePrettiesAs`
          "unknown"
    , TypedValue (TVStringArray ["Plexil_Unknown", "normal", "Plexil_Unknown"])
        `testValuePrettiesAs`
          "array(unknown # val(\"normal\") # unknown)"
    ]
  ]
  where
  testItParsesAs :: String -> Value -> TestTree
  testItParsesAs str cmd = testCase (show cmd) $ str `parsesOnlyAs` cmd

  testItPicklesAs :: Value -> String -> TestTree
  testItPicklesAs cmd str = testCase (show cmd) $ cmd `isPickledAs` str

  testValuePrettiesAs :: Value -> String -> TestTree
  testValuePrettiesAs v str =
    testCase (show v) $
      assertEqual "is not pretty printed as"
        (text str)
        (pretty v)

testState :: TestTree
testState = testGroup "State"
  [ testGroup "fromXML"
    [
          State "st" [] [ Value { unValue = "1" }, Value { unValue = "2" }, Value { unValue = "3" }] PXIntArray
            `testPrettiesAs`
              "stateLookup('st,nilarg,array(val(1) # val(2) # val(3)))"
    ,
          State "st" [] [ Value { unValue = "1" }] PXInt
            `testPrettiesAs`
              "stateLookup('st,nilarg,val(1))"
    ,
          State "st" [] [ Value { unValue = "one" }] PXString
            `testPrettiesAs`
               [r|stateLookup('st,nilarg,val("one"))|]
    ,
          State "st" [] [ Value { unValue = "one" }, Value { unValue = "two" }] PXString
            `testPrettiesAs`
               [r|stateLookup('st,nilarg,val("one"))|]
    ,
          State "st" [Parameter "1" PXInt] [ Value { unValue = "one" }, Value { unValue = "two" }] PXString
            `testPrettiesAs`
               [r|stateLookup('st,(val(1)),val("one"))|]
    ,
          State "st" [Parameter "1" PXReal ,Parameter "10" PXInt] [ Value { unValue = "one" }, Value { unValue = "two" }] PXString
            `testPrettiesAs`
               [r|stateLookup('st,(val(float(1)) val(10)),val("one"))|]
    ,
          State "st" [] [ Value { unValue = "Plexil_Unknown" }] PXString
            `testPrettiesAs`
               "stateLookup('st,nilarg,unknown)"
    ,
          State "st" [] [ Value { unValue = "Plexil_Unknown" }] PXInt
            `testPrettiesAs`
               "stateLookup('st,nilarg,unknown)"
    ,
          State "st" [] [ Value { unValue = "1" }, Value { unValue = "Plexil_Unknown" }, Value { unValue = "3" }] PXIntArray
            `testPrettiesAs`
              "stateLookup('st,nilarg,array(val(1) # unknown # val(3)))"
    ]
  ]
  where
    testPrettiesAs :: forall a. (Pretty a,Show a) => a -> String -> TestTree
    testPrettiesAs p str =
      testCase (show p) $
        assertEqual "is not pretty printed as"
          (text str)
          (pretty p)

testSimultaneous :: TestTree
testSimultaneous = testGroup "Simultaneous"
  [ testGroup "fromXML"
    [
      [r|<Simultaneous><State name="time" type="real"><Value>0.5</Value></State><State name="city" type="string"><Value>Valencia</Value></State></Simultaneous>|]
        `testItParsesAs`
          Simultaneous [
                          SimultaneousEntry { unSimultaneousEntry = OneState $ State { stName = "time"
                                                                                      , stParams = []
                                                                                      , stValue = [Value { unValue = "0.5" }]
                                                                                      , stType = PXReal
                                                                                      }
                                            }
                        , SimultaneousEntry { unSimultaneousEntry = OneState $ State { stName = "city"
                                                                                      , stParams = []
                                                                                      , stValue = [Value { unValue = "Valencia" }]
                                                                                      , stType = PXString
                                                                                      }
                                            }
                        ]
    ]
  ]
  where
    testItParsesAs :: String -> Simultaneous -> TestTree
    testItParsesAs str cmd = testCase (show cmd) $ str `parsesOnlyAs` cmd

    testItPicklesAs :: Simultaneous -> String -> TestTree
    testItPicklesAs cmd str = testCase (show cmd) $ cmd `isPickledAs` str

testCommandHandles :: TestTree
testCommandHandles = testGroup "Command Handles"
  [ testGroup "from XML"
    [ "<Result>COMMAND_DENIED</Result>"         `testItParsesAs` CommandDenied
    , "<Result>COMMAND_ACCEPTED</Result>"       `testItParsesAs` CommandAccepted
    , "<Result>COMMAND_SENT_TO_SYSTEM</Result>" `testItParsesAs` CommandSentToSystem
    , "<Result>COMMAND_RCVD_BY_SYSTEM</Result>" `testItParsesAs` CommandReceivedBySystem
    , "<Result>COMMAND_SUCCESS</Result>"        `testItParsesAs` CommandSuccess
    , "<Result>COMMAND_FAILED</Result>"         `testItParsesAs` CommandFailed
    , testItDoesNotParse "<Result>COMMAND_denied</Result>"
    , testItDoesNotParse "<result>COMMAND_DENIED</Result>"
    , testItDoesNotParse "<Result>COMMAND_ACCEPTED</result>"
    , testItDoesNotParse "<Result>command_sent_to_system</Result>"
    , testItDoesNotParse "<Result>COMMAND</Result>"
    , testItDoesNotParse "<Result>SUCCESS</Result>"
    , testItDoesNotParse "<Result>FAILED</Result>"
    ]
  , testGroup "to XML"
    [ CommandDenied           `testItPicklesAs` "<Result>COMMAND_DENIED</Result>"
    , CommandAccepted         `testItPicklesAs` "<Result>COMMAND_ACCEPTED</Result>"
    , CommandSentToSystem     `testItPicklesAs` "<Result>COMMAND_SENT_TO_SYSTEM</Result>"
    , CommandReceivedBySystem `testItPicklesAs` "<Result>COMMAND_RCVD_BY_SYSTEM</Result>"
    , CommandSuccess          `testItPicklesAs` "<Result>COMMAND_SUCCESS</Result>"
    , CommandFailed           `testItPicklesAs` "<Result>COMMAND_FAILED</Result>"
    ]
  ]
  where
    anyCommandHandle :: CommandHandle
    anyCommandHandle = undefined

    testItParsesAs :: String -> CommandHandle -> TestTree
    testItParsesAs str cmdHandle = testCase (show cmdHandle) $ str `parsesOnlyAs` cmdHandle

    testItDoesNotParse :: String -> TestTree
    testItDoesNotParse str = testCase "It does not parse" $ str `doesNotParseAs` anyCommandHandle

    testItPicklesAs :: CommandHandle -> String -> TestTree
    testItPicklesAs cmdHandle str = testCase (show cmdHandle) $ cmdHandle `isPickledAs` str

testUpdateAck :: TestTree
testUpdateAck = testGroup "UpdateAck"
  [ testGroup "from XML"
    [ [r|<UpdateAck name="array8"/>|]
        `testItParsesAs`
          UpdateAck { uaName = "array8", uaBool = True }
    ]
  ]
  where
    testItParsesAs :: String -> UpdateAck -> TestTree
    testItParsesAs str cmd = testCase (show cmd) $ str `parsesOnlyAs` cmd

    testItPicklesAs :: UpdateAck -> String -> TestTree
    testItPicklesAs cmd str = testCase (show cmd) $ cmd `isPickledAs` str

testDelay :: TestTree
testDelay = testGroup "Delay"
  [ [r|<Delay/>|]
      `testItParsesAs`
        Delay ()
  , [r|<Delay></Delay>|]
      `testItParsesAs`
        Delay ()
  , Delay ()
      `testItPicklesAs`
        "<Delay/>"
  ]
  where
    testItParsesAs :: String -> Delay -> TestTree
    testItParsesAs str cmd = testCase (show cmd) $ str `parsesOnlyAs` cmd

    testItPicklesAs :: Delay -> String -> TestTree
    testItPicklesAs cmd str = testCase (show cmd) $ cmd `isPickledAs` str

testScript :: TestTree
testScript = testGroup "Script"
  [ testGroup "from XML"
    [ [r|<Script><UpdateAck name="array8"/></Script>|]
        `testItParsesAs`
          Script [ ScriptEntry { unScriptEntry = FiveOf7 $ UpdateAck { uaName = "array8", uaBool = True } } ]
    ]
  ]
  where
    testItParsesAs :: String -> Script -> TestTree
    testItParsesAs str cmd = testCase (show cmd) $ str `parsesOnlyAs` cmd

    testItPicklesAs :: Script -> String -> TestTree
    testItPicklesAs cmd str = testCase (show cmd) $ cmd `isPickledAs` str

parsesOnlyAs :: (XmlPickler a,Eq a,Show a) => String -> a -> Assertion
parsesOnlyAs str expectedData =
  do
    results <- runX ( readString [withErrors no] str >>> arr (unpickleDoc' xpickle) )
    case results of
      [Right  parsedData] -> assertEqual "Incorrectly parsed: " expectedData parsedData
      [Left errorMessage] -> assertFailure $ "Incorrectly parsed " ++ errorMessage
      []                  -> assertFailure $ "No parsing for " ++ show str
      _                   -> assertFailure $ "Many parses for " ++ show results


doesNotParseAs :: forall a. (XmlPickler a,Eq a,Show a) => String -> a -> Assertion
doesNotParseAs str _ =
  do
    results <- runX ( readString [withErrors no] str >>> arr (unpickleDoc' (xpickle :: PU a)) )
    case results of
      [Right  parsedData] -> assertFailure $
                                  "Incorrectly parsed " ++ show str
                                  ++ " as '" ++ show parsedData ++ "'"
      _                   -> return ()

isPickledAs :: (XmlPickler a,Eq a,Show a) => a -> String ->Assertion
isPickledAs a expectedStr = assertEqual "Incorrect serialization: " expectedStr pickledA
  where
    pickledA :: String
    pickledA = showPickled [] a