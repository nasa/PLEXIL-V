{-# LANGUAGE FlexibleInstances #-}
{-# LANGUAGE OverloadedStrings #-}
{-# LANGUAGE QuasiQuotes #-}

module Main where

import Parser
import Control.Applicative
import Control.Monad.Except
import Data.Char
import Data.Either
import Data.Maybe
-- import Data.List (intersperse)
-- import qualified Data.Map as M
import Data.String (fromString)
-- import Data.Text (Text) --  hiding (map)
-- import Debug.Trace
-- import qualified Data.Text as T --  hiding (map)
import Prelude hiding ((<>)) -- (concat)
-- import System.Environment
-- import System.Exit
-- import Data.Text.Internal.Lazy
import Test.Tasty
import Test.Tasty.HUnit
import Text.PrettyPrint
-- import qualified Text.PrettyPrint as PP
import Text.RawString.QQ
import Text.XML hiding (Name)
-- import qualified Text.XML as XML
import Text.XML.Cursor

import Benchmarks(testBenchmarks)
import PSX2MaudeTests(testPSX2Maude)
import TestArrays(testArrays)
import TestCommon
import TestLibraryCall (testLibraryCall)
import TestNodeRef(testNodeRef)
import LibraryCallExpanderTests (testLibraryCallExpander)

main :: IO ()
main = defaultMain $
  testGroup "Tests"
    [testsLegacy
    ,testLibraryCall
    ,testLibraryCallExpander
    ,testBenchmarks
    ,testPSX2Maude
    ,testArrays
    ,testNodeRef
    ,testsRegression
    ,testGroup "regression tests" $ testParser elementVisitor [
      ("command1.ple", [r|
<PlexilPlan xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" FileName="command1.ple">
  <Node ColNo="0" LineNo="1" NodeType="Command">
    <NodeId>command1</NodeId>
    <VariableDeclarations>
      <DeclareVariable ColNo="2" LineNo="3">
        <Name>CommandName</Name>
        <Type>String</Type>
        <InitialValue>
          <StringValue>foo</StringValue>
        </InitialValue>
      </DeclareVariable>
    </VariableDeclarations>
    <NodeBody>
      <Command ColNo="3" LineNo="5">
        <Name>
          <StringVariable>CommandName</StringVariable>
        </Name>
        <Arguments ColNo="16" LineNo="5">
          <StringValue />
        </Arguments>
      </Command>
    </NodeBody>
  </Node>
</PlexilPlan>
    |], "modcommand1-PLANisprotectingPLEXIL-V.oprootNode:->Plexil.eqrootNode=command('command1,(('CommandName:val(\"foo\"))),(none),((cmdId(var('CommandName)))/(const(val(\"\")))/nothing)).endm")
    ]
    ]

testsRegression :: TestTree
testsRegression =
  testGroup "commands"
    [testGroup "pieces"
      [testGroup "parseCommand'" $
        testErrorParser parseCommand'
          [("1", [r|
<Command ColNo="3" LineNo="5">
  <Name>
    <StringVariable>CommandName</StringVariable>
  </Name>
  <Arguments ColNo="16" LineNo="5">
    <StringValue />
  </Arguments>
</Command>|], "((cmdId(var('CommandName)))/(const(val(\"\")))/nothing)")
          ]
      ,testGroup "parseNameFromStringVariable" $
        testStringErrorParser parseNameFromStringVariable
          [("2", [r|
    <Name>
      <StringVariable>CommandName</StringVariable>
    </Name>|],"cmdId(var('CommandName))")
          ]
      ]
    ]

testsLegacy :: TestTree
testsLegacy =
    testGroup "Legacy Tests"
        [testsParseBooleanExpression
        ,testsParseNodeStateValue
        ,testsParseNodeStateVariable
        ,testsParseNodeOutcomeVariable
        ,testsParseNodeState
        ,testsPrettyOutcomeEq
        ,testsPrettyStateEq
        ,testsBinarizeList
        ,testsParseNodeCondition
        ,testLookups
        ,testArithmeticExpressions
        ,testUpdate
        ,testsParseConcat
        ,testGroup "Different issues" $
          map (testify'' elementVisitor)
            [("a failing end condition",
              [r|
                <EndCondition>
                  <EQInternal>
                    <NodeCommandHandleVariable>
                      <NodeRef dir="self" />
                    </NodeCommandHandleVariable>
                    <NodeCommandHandleValue>COMMAND_SUCCESS</NodeCommandHandleValue>
                  </EQInternal>
                </EndCondition>
              |],"(endc:(cmdHandleIs?(self,CommandSuccess)))")
            , ("a self reference",
              [r|
                <PostCondition ColNo="6" LineNo="7">
                        <Skipped ColNo="20" LineNo="7">
                            <NodeRef dir="self" />
                        </Skipped>
                    </PostCondition>
              |],"(post: (hasSkipped?(self)))")
            ]
        ,testGroup "Parse internal equality expression" [testify'' elementVisitor ("An icarous node failure equality expression ",
                  [r|
                     <EQInternal>
                       <NodeFailureVariable>
                         <NodeRef dir="sibling">ep2cp_IfTest</NodeRef>
                       </NodeFailureVariable>
                       <NodeFailureValue>POST_CONDITION_FAILED</NodeFailureValue>
                     </EQInternal>
                      |],
                  [r|isFailure?('ep2cp-IfTest,postconditionFailed)|])]
        ,testGroup "Parse variable declarations" $
            map (testify'' elementVisitor)
                [("A simple real variable declaration",
                  [r|
                     <VariableDeclarations>
                       <DeclareVariable>
                         <Name>r1</Name>
                         <Type>Real</Type>
                       </DeclareVariable>
                     </VariableDeclarations>
                    |],
                  [r| ( ('r1 : unknown) ) |])
                ,("A simple string variable declaration",
                  [r|
                     <VariableDeclarations>
                       <DeclareVariable>
                         <Name>r1</Name>
                         <Type>String</Type>
                       </DeclareVariable>
                     </VariableDeclarations>
                    |],
                  [r| ( ('r1 : unknown) ) |])
                ,("A simple integer variable declaration",
                  [r|
                     <VariableDeclarations>
                       <DeclareVariable>
                         <Name>r1</Name>
                         <Type>Integer</Type>
                       </DeclareVariable>
                     </VariableDeclarations>
                    |],
                  [r| ( ('r1 : unknown) ) |])
                ,("A simple boolean variable declaration",
                  [r|
                     <VariableDeclarations>
                       <DeclareVariable>
                         <Name>r1</Name>
                         <Type>Boolean</Type>
                       </DeclareVariable>
                     </VariableDeclarations>
                    |],
                  [r| ( ('r1 : unknown) ) |])
                ,("A simple variable declaration with initialiation",
                  [r|
                     <VariableDeclarations>
                       <DeclareVariable LineNo="6" ColNo="2">
                         <Name>i</Name>
                         <Type>Integer</Type>
                         <InitialValue>
                           <IntegerValue>0</IntegerValue>
                         </InitialValue>
                       </DeclareVariable>
                     </VariableDeclarations>
                    |],
                  [r| ( ('i : val(0)) ) |])
                ,("An icarous array declaration",
                  [r|
                     <DeclareArray LineNo="23" ColNo="4">
                       <Name>acPosition</Name>
                       <Type>Real</Type>
                       <MaxSize>3</MaxSize>
                     </DeclareArray>|],
                  [r| ('acPosition:createArray(3,unknownArray(3))) |])
                ,("An icarous array declaration with explicit initialization",
                  [r|
                     <DeclareArray LineNo="4" ColNo="2">
                       <Name>bar</Name>
                       <Type>Real</Type>
                       <MaxSize>3</MaxSize>
                       <InitialValue>
                         <RealValue>0</RealValue>
                         <RealValue>7</RealValue>
                         <RealValue>13</RealValue>
                       </InitialValue>
                     </DeclareArray>|],
                  [r| ('bar:createArray(3,val(0.0)#val(7.0)#val(13.0))) |])
                  ,("An empty variable declaration",
                  [r|
                     <DeclareVariable ColNo="4" LineNo="3">
                      <Name>foo</Name>
                      <Type>String</Type>
                      <InitialValue>
                        <StringValue />
                      </InitialValue>
                    </DeclareVariable>
                    |],
                    [r| ('foo : val("")) |])
                ]
        ,testGroup "Parse initial value" $
            testErrorParser parseInitialSimpleValue
                [("Empty initial value",
                  [r|
                    <InitialValue>
                      <StringValue />
                    </InitialValue>
                    |],
                  [r| val("") |])
                ]
        ,testGroup "Parse an array element" [testify'' elementVisitor ("A simple array element",
                  [r|
                     <ArrayElement>
                       <ArrayVariable>foo</ArrayVariable>
                       <Index>
                         <IntegerVariable>i</IntegerVariable>
                       </Index>
                     </ArrayElement>
                    |],
                  [r| arrayVar('foo,var('i)) |])]
        ,testGroup "Parse an empty node" [testify'' elementVisitor ("An icarous Empty node",
                  [r|
                     <Node NodeType="Empty" epx="Condition">
                       <NodeId>ep2cp_IfTest</NodeId>
                       <PostCondition>
                         <GE>
                           <RealVariable>speedPref</RealVariable>
                           <IntegerValue>0</IntegerValue>
                         </GE>
                       </PostCondition>
                     </Node>|],
                  [r|
                    empty(
                      'ep2cp-IfTest,
                      nilocdecl,
                      ((post: (_>=_(var('speedPref),const(val(0))))))
                    )|])]
        ,testGroup "Parse an assignment node" $
            map (testify'' elementVisitor)
                [("A simple assignment node",
                  [r|
                     <Node NodeType="Assignment" LineNo="13" ColNo="4">
                       <NodeId>ASSIGNMENT__0</NodeId>
                       <NodeBody>
                         <Assignment>
                           <RealVariable>r1</RealVariable>
                           <NumericRHS>
                             <LookupNow>
                               <Name>
                                 <StringValue>r1</StringValue>
                               </Name>
                             </LookupNow>
                           </NumericRHS>
                         </Assignment>
                       </NodeBody>
                     </Node>|],
                  [r|
                    assignment(
                      'ASSIGNMENT--0,
                      nilocdecl,
                      ( none ),
                      (var('r1) := lookup ('r1 , (nilarg)))
                    )|])
                ,("A simple array assignment node",
                  [r|
                     <Node NodeType="Assignment" LineNo="11" ColNo="27">
                       <NodeId>SimpleArrayAssignment1</NodeId>
                       <NodeBody>
                         <Assignment>
                           <ArrayElement>
                             <ArrayVariable>foo</ArrayVariable>
                             <Index>
                               <IntegerVariable>i</IntegerVariable>
                             </Index>
                           </ArrayElement>
                           <NumericRHS>
                             <RealValue>1.0</RealValue>
                           </NumericRHS>
                         </Assignment>
                       </NodeBody>
                     </Node>
                    |],
                  [r|
                    assignment(
                      'SimpleArrayAssignment1,nilocdecl,(none),(arrayVar('foo,var('i)):=const(val(1.0)))
                    )
                    |])
                ,("An icarous complex array assignment node",
                  [r|
                     <Assignment>
                       <ArrayElement>
                         <ArrayVariable>velCmd</ArrayVariable>
                         <Index>
                           <IntegerValue>0</IntegerValue>
                         </Index>
                       </ArrayElement>
                       <NumericRHS>
                         <ArrayElement>
                           <ArrayVariable>acVelocity</ArrayVariable>
                           <Index>
                             <IntegerValue>0</IntegerValue>
                           </Index>
                         </ArrayElement>
                       </NumericRHS>
                     </Assignment>
                    |],
                  [r|
                       ( arrayVar('velCmd,const(val(0))):=(arrayVar('acVelocity,const(val(0)))) )
                    |])

                ]
        ,testGroup "Parse a command node" $
            map (testify'' elementVisitor)
                [("A simple command node",
                  [r|
                     <Node NodeType="Command">
                       <NodeId>Example1</NodeId>
                       <StartCondition>
                         <BooleanValue>true</BooleanValue>
                       </StartCondition>
                       <NodeBody>
                         <Command>
                           <Name>
                             <StringValue>pprint</StringValue>
                           </Name>
                           <Arguments LineNo="40" ColNo="11">
                             <StringValue>r:</StringValue>
                             <RealVariable>r</RealVariable>
                           </Arguments>
                         </Command>
                       </NodeBody>
                     </Node>|],
                  [r|
                    command(
                      'Example1,
                      nilocdecl,
                      ( (startc: (const(val(true)))) ),
                      ( ('pprint) / ( const(val("r:")) var('r) ) / nothing )
                    )|])
                ,("A complex command node",
                  [r|
                     <Node NodeType="Command" LineNo="34" ColNo="4">
                       <NodeId>Printer0</NodeId>
                       <StartCondition>
                         <BooleanValue>false</BooleanValue>
                       </StartCondition>
                       <EndCondition>
                         <AND>
                           <EQInternal>
                             <NodeStateVariable>
                               <NodeRef dir="sibling">TestReal__2</NodeRef>
                             </NodeStateVariable>
                             <NodeStateValue>FINISHED</NodeStateValue>
                           </EQInternal>
                           <EQInternal>
                             <NodeStateVariable>
                               <NodeId>TestVars1</NodeId>
                             </NodeStateVariable>
                             <NodeStateValue>FINISHED</NodeStateValue>
                           </EQInternal>
                         </AND>
                       </EndCondition>
                       <NodeBody>
                         <Command>
                           <Name>
                             <StringValue>pprint</StringValue>
                           </Name>
                           <Arguments LineNo="35" ColNo="11">
                             <StringValue>r1:</StringValue>
                             <RealVariable>r1</RealVariable>
                             <StringValue>r2:</StringValue>
                             <RealVariable>r2</RealVariable>
                           </Arguments>
                         </Command>
                       </NodeBody>
                     </Node>|],
                  [r|
                    command(
                      'Printer0,
                      nilocdecl,
                      ( (startc: (const(val(false)))),
                        (endc: (_and_(isStatus?('TestReal--2,finished),isStatus?('TestVars1,finished))))
                      ),
                      ( ('pprint) / ( const(val("r1:")) var('r1) const(val("r2:")) var('r2) ) / nothing )
                    )|])
                ,("A complex command node with return value",
                  [r|
                      <Node ColNo="4" LineNo="6" NodeType="Command">
                        <NodeId>BLOCK__0</NodeId>
                        <NodeBody>
                            <Command ColNo="8" LineNo="7">
                                <RealVariable>ret</RealVariable>
                                <Name>
                                    <StringValue>complexCommand</StringValue>
                                </Name>
                                <Arguments ColNo="29" LineNo="7">
                                    <RealVariable>ret</RealVariable>
                                </Arguments>
                            </Command>
                        </NodeBody>
                      </Node>|],
                  [r|
                    command(
                      'BLOCK--0,
                      nilocdecl,
                      (none),
                      ( ('complexCommand) / (var('ret)) / just('ret) )
                    )|])
              ]
        ,testGroup "Parse a node body" $
            map (testify'' elementVisitor)
                [("A command node body",
                  [r|
                     <NodeBody>
                       <Command>
                         <Name>
                           <StringValue>pprint</StringValue>
                         </Name>
                         <Arguments LineNo="40" ColNo="11">
                           <StringValue>r:</StringValue>
                           <RealVariable>r</RealVariable>
                         </Arguments>
                       </Command>
                     </NodeBody>|],
                  "( ('pprint) / ( const(val(\"r:\")) var('r) ) / nothing )")
                ,("An assignment node body",
                  [r|
                     <NodeBody>
                       <Assignment>
                         <RealVariable>r1</RealVariable>
                         <NumericRHS>
                           <LookupNow>
                             <Name>
                               <StringValue>r1</StringValue>
                             </Name>
                           </LookupNow>
                         </NumericRHS>
                       </Assignment>
                     </NodeBody>|],
                  "(var('r1) := lookup ('r1 , (nilarg)))")
                ]
        ,testGroup "Parse a command" $
            map (testify'' elementVisitor)
                [("Simple command",
                  [r|
                     <Command>
                       <Name>
                         <StringValue>pprint</StringValue>
                       </Name>
                       <Arguments LineNo="40" ColNo="11">
                         <StringValue>r:</StringValue>
                         <RealVariable>r</RealVariable>
                       </Arguments>
                     </Command>|],
                  "( ('pprint) / ( const(val(\"r:\")) var('r) ) / nothing )")
                ,("Simple command with assignment",
                  [r|
                     <Command>
                       <RealVariable>r</RealVariable>
                       <Name>
                         <StringValue>whatever</StringValue>
                       </Name>
                       <Arguments LineNo="40" ColNo="11">
                         <StringValue>r:</StringValue>
                         <RealVariable>r</RealVariable>
                       </Arguments>
                     </Command>|],
                  "( ('whatever) / ( const(val(\"r:\")) var('r) ) / just('r) )")
                ,("Another simple command with assignment",
                  [r|
                     <Command>
                       <RealVariable>r</RealVariable>
                       <Name>
                         <StringValue>get_real</StringValue>
                       </Name>
                     </Command>|],
                  "( ('get_real) / ( nilpar ) / just('r) )")
                ,("An icarous command with assignment",
                  [r|
                     <Command>
                       <Name>
                         <StringValue>SetVel</StringValue>
                       </Name>
                       <Arguments LineNo="86" ColNo="22">
                         <ArrayVariable>velCmd</ArrayVariable>
                       </Arguments>
                     </Command>
                     |],
                  "( ('SetVel) / (arrayVar('velCmd)) / nothing )")
                ]
        ,testGroup "Parse a name" [testify'' elementVisitor ("Name with a string value element",
                  [r|
                    <Name>
                      <StringValue>pprint</StringValue>
                    </Name>|],
                  "'pprint")]
        ,testGroup "Parse a RealValue with no decimals" $
            map (testify'' elementVisitor)
                [("1",
                  [r|
                    <RealValue>1</RealValue>|],
                  "const(val(1.0))")
                ,("Realvalue in assignment",
                  [r|<Assignment ColNo="16" LineNo="160">
                      <ArrayElement>
                        <ArrayVariable>velCmd</ArrayVariable>
                        <Index>
                          <IntegerValue>2</IntegerValue>
                        </Index>
                      </ArrayElement>
                      <NumericRHS>
                        <RealValue>0</RealValue>
                      </NumericRHS>
                    </Assignment>|],
                  "(arrayVar('velCmd,const(val(2))):=const(val(0.0)))")
                ,("RealValue 1000",
                  [r|
                    <RealValue>1000</RealValue>|],
                  "const(val(1000.0))")
                ,( "RealValue 1000.0",
                  [r|
                    <RealValue>1000.0</RealValue>|],
                  "const(val(1000.0))")
                ,("RealValue -100",
                  [r|
                    <RealValue>-100</RealValue>|],
                  "const(val(-100.0))")
                ,("RealValue -1e2",
                  [r|
                    <RealValue>-1e2</RealValue>|],
                  "const(val(-100.0))")
                ]
          ,testGroup "Parse a real array with integervalues" $
            map (testify'' elementVisitor)
                [("Array with 3 elements",
                  [r|
                    <DeclareArray>
                      <Name>a1</Name>
                      <Type>Real</Type>
                      <MaxSize>10</MaxSize>
                      <InitialValue>
                        <ArrayValue Type="Real">
                          <IntegerValue>1</IntegerValue>
                          <IntegerValue>2</IntegerValue>
                          <IntegerValue>3</IntegerValue>
                        </ArrayValue>
                      </InitialValue>
                    </DeclareArray>|],
                  "('a1 : createArray(10, val(1.0) # val(2.0) # val(3.0)))")
                ,("Array with 3 elements 2'",
                  [r|
                    <DeclareArray>
                      <Name>a1</Name>
                      <Type>Real</Type>
                      <MaxSize>10</MaxSize>
                      <InitialValue>
                          <IntegerValue>1</IntegerValue>
                          <IntegerValue>2</IntegerValue>
                          <IntegerValue>3</IntegerValue>
                      </InitialValue>
                    </DeclareArray>|],
                  "('a1 : createArray(10, val(1.0) # val(2.0) # val(3.0)))")
                ]
        ]

type TestEntry = (TestName,String,String)

testify' :: (Cursor -> TextOrError) -> TestEntry -> TestTree
testify' f (msg,i,o) = testCase msg $
    if fromString o /= ("" :: String)
      then test f i @?= Right (fromString o)
      else assertBool "returned value should be error (Left)" $ isLeft $ test f i

testify'' :: (Cursor -> Doc) -> TestEntry -> TestTree
testify'' f (msg,i,o) = testCase msg $
    clean (renderStyle (style {mode = OneLineMode}) (test f i)) @?= clean (renderStyle (style {mode = OneLineMode}) (text (fromString o)))
    where clean = filter (not . isSpace)

testify''' :: (Cursor -> ParseError Doc) -> TestEntry -> TestTree
testify''' f (msg,i,o) = testCase msg $
    test f i @?= Right (text (fromString o))

test :: (Cursor -> t) -> String -> t
test f str = f cursor
    where
        doc = parseText_ def $ fromString str
        cursor = fromDocument doc

testify :: (Eq a, Show a) => (Cursor -> Maybe a) -> (TestName, String, a) -> TestTree
testify f (msg,i,o) = testCase msg $ test f i @?= Just o


testsParseNodeStateValue :: TestTree
testsParseNodeStateValue =
    testGroup "parseNodeStateValue" $
        map (testify'' elementVisitor) testsParseNodeStateValueTable

testsParseNodeStateValueTable :: [TestEntry]
testsParseNodeStateValueTable =
    [("Waiting",        "<NodeStateValue>WAITING</NodeStateValue>",         "waiting"       )
    ,("Executing",      "<NodeStateValue>EXECUTING</NodeStateValue>",       "executing"     )
    ,("Finishing",      "<NodeStateValue>FINISHING</NodeStateValue>",       "finishing"     )
    ,("Failing",        "<NodeStateValue>FAILING</NodeStateValue>",         "failing"       )
    ,("IterationEnded", "<NodeStateValue>ITERATION_ENDED</NodeStateValue>", "iterationEnded")
    ,("Finished",       "<NodeStateValue>FINISHED</NodeStateValue>",        "finished"      )
    ,("Inactive",       "<NodeStateValue>INACTIVE</NodeStateValue>",        "inactive"      )
    ]

testsParseNodeStateVariable :: TestTree
testsParseNodeStateVariable =
    testGroup "parseNodeStateVariable" $
        map (testify' parseNodeStateVariable)
            [("Simple child identifier", "<NodeStateVariable><NodeRef dir=\"child\">Node__Identifier</NodeRef></NodeStateVariable>", "Node--Identifier")
            ,("Other stuff", "<NodeStateValue>FAILING</NodeStateValue>", "")
            ]

testsParseNodeState :: TestTree
testsParseNodeState =
    testGroup "parseNodeState" $
        map (testify' parseNodeState)
            [("Identifier", "<NodeStateVariable><NodeRef dir=\"child\">NodeIdentifier</NodeRef></NodeStateVariable>", "NodeIdentifier")
            ,("StateValue", "<NodeStateValue>FAILING</NodeStateValue>", "failing")
            ]

testsParseConcat :: TestTree
testsParseConcat =
    testGroup "parseConcat" $
        map (testify'' elementVisitor)
            [("2-concat", [r|
              <Concat ColNo="47" LineNo="11">
                <StringValue>one</StringValue>
                <StringValue>two</StringValue>
              </Concat>
            |],[r|(const(val("one")) + const(val("two")))|])
            ,("3-concat", [r|
              <Concat ColNo="47" LineNo="11">
                <StringValue>one</StringValue>
                <StringValue>two</StringValue>
                <StringValue>three</StringValue>
              </Concat>
            |],[r|(const(val("one")) + (const(val("two")) + const(val("three"))))|])
            ,("4-concat", [r|
              <Concat ColNo="47" LineNo="11">
                <StringValue>one</StringValue>
                <StringValue>two</StringValue>
                <StringValue>three</StringValue>
                <StringValue>four</StringValue>
              </Concat>
            |],[r|(const(val("one")) + (const(val("two")) + (const(val("three")) + const(val("four")))))|])
            ,("3-concat with var", [r|
              <Concat ColNo="47" LineNo="11">
                <StringValue>one</StringValue>
                <StringValue>two</StringValue>
                <StringVariable>bar</StringVariable>
              </Concat>
            |],[r|(const(val("one")) + (const(val("two")) + var('bar)))|])
            ]

testsParseNodeOutcomeVariable :: TestTree
testsParseNodeOutcomeVariable =
    testGroup "parseNodeOutcomeVariable" $
        map (testify'' elementVisitor)
            [("Simple child identifier with NodeRef", "<NodeOutcomeVariable><NodeRef dir=\"child\">Printer0</NodeRef></NodeOutcomeVariable>", "Printer0"),
             ("Simple child identifier with NodeId", "<NodeOutcomeVariable><NodeId>callBoolArrayCommand</NodeId></NodeOutcomeVariable>", "callBoolArrayCommand")
            ]

testsParseBooleanExpression :: TestTree
testsParseBooleanExpression =
  testGroup
    "parseBooleanExpression" $
        map (testify'' elementVisitor)
            [("BooleanValue true",
              "<BooleanValue>true</BooleanValue>"
              ,"const(val(true))")
            ,("BooleanValue false",
              "<BooleanValue>false</BooleanValue>",
              "const(val(false))")
            ,("BooleanVariable",
              "<BooleanVariable>Myvar</BooleanVariable>","var('Myvar)")
            ,("KnownTest IsKnown",
              "<IsKnown><BooleanValue>true</BooleanValue></IsKnown>",
              "isKnown(const(val(true)))")
            ,("LogicalOperator OR",
              "<OR><BooleanValue>true</BooleanValue><BooleanValue>false</BooleanValue><BooleanValue>true</BooleanValue></OR>",
              "_or_(_or_(const(val(true)),const(val(false))),const(val(true)))")
            ,("LogicalOperator AND",
              "<AND><BooleanValue>true</BooleanValue><BooleanValue>true</BooleanValue><BooleanValue>false</BooleanValue></AND>",
              "_and_(_and_(const(val(true)),const(val(true))),const(val(false)))")
            ,("LogicalOperator AND",
              "<AND><BooleanValue>true</BooleanValue><BooleanValue>true</BooleanValue><BooleanValue>false</BooleanValue></AND>",
              "_and_(_and_(const(val(true)),const(val(true))),const(val(false)))")
            ,("LogicalOperator XOR",
              "<XOR><BooleanValue>true</BooleanValue><BooleanValue>true</BooleanValue><BooleanValue>false</BooleanValue></XOR>",
              "_xor_(_xor_(const(val(true)),const(val(true))),const(val(false)))")
            ,("LogicalOperator NOT",
              "<NOT><BooleanValue>false</BooleanValue></NOT>",
              "not_(const(val(false)))")
            ,("Equality EQBoolean",
              "<EQBoolean><BooleanValue>true</BooleanValue><BooleanValue>false</BooleanValue></EQBoolean>",
              "_equ_(const(val(true)),const(val(false)))")
            ,("Equality NEBoolean",
              "<NEBoolean><BooleanValue>true</BooleanValue><BooleanValue>false</BooleanValue></NEBoolean>",
              "_nequ_(const(val(true)),const(val(false)))")
            ,("Equality EQNumeric",
              "<EQNumeric><IntegerValue>3</IntegerValue><IntegerValue>4</IntegerValue></EQNumeric>",
              "_equ_(const(val(3)),const(val(4)))")
            ,("Equality EQInternal",
              "<EQNumeric><IntegerValue>3</IntegerValue><IntegerValue>4</IntegerValue></EQNumeric>",
              "_equ_(const(val(3)),const(val(4)))")
            ,("Non-Equality NENumeric",
              "<NENumeric><IntegerValue>3</IntegerValue><IntegerValue>4</IntegerValue></NENumeric>",
              "_nequ_(const(val(3)),const(val(4)))")
            ,("Equality EQString",
              "<EQString><StringValue>a</StringValue><StringValue>b</StringValue></EQString>",
              "_equ_(const(val(\"a\")),const(val(\"b\")))")
            ,("Non-Equality NEString",
              "<NEString><StringValue>a</StringValue><StringValue>b</StringValue></NEString>",
              "_nequ_(const(val(\"a\")),const(val(\"b\")))")
            ,("NoChildFailed",
              [r|
                <NoChildFailed>
                  <NodeRef dir="self"/>
                </NoChildFailed>|],
              "noChildFailed")
            ,("Finished",
              [r|
                <Finished>
                  <NodeRef dir="sibling">ASSIGNMENT__0</NodeRef>
                </Finished>|],
              "(isFinished?(sibling('ASSIGNMENT--0)))")
            ,("Finished2",
              [r|
                <Finished ColNo="15" LineNo="10">
                  <NodeId>ConjunctTest1</NodeId>
                </Finished>|],
              "(isFinished?('ConjunctTest1))")
            ,("Succeeded",
              [r|
                <Succeeded>
                  <NodeRef dir="sibling">ep2cp_IfTest</NodeRef>
                </Succeeded>|],
              "hasSucceeded?(sibling('ep2cp-IfTest))")
            ,("PostconditionFailed",
              [r|
                <PostconditionFailed>
                  <NodeRef dir="sibling">ep2cp_IfTest</NodeRef>
                </PostconditionFailed>
               |],
              "hasPostconditionFailed?(sibling('ep2cp-IfTest))")
            ,("Skipped",
              [r|
                <Skipped>
                  <NodeRef dir="sibling">ep2cp_ElseIf-1</NodeRef>
                </Skipped>
               |],
              "hasSkipped?(sibling('ep2cp-ElseIf-1))")


            ]

testsPrettyOutcomeEq :: TestTree
testsPrettyOutcomeEq =
  testGroup
    "Node Outcome Equality" $
        map (testify'' elementVisitor)
            [("FAILURE",
              [r|   <EQInternal>
                        <NodeOutcomeVariable>
                            <NodeRef dir="child">TestVars1</NodeRef>
                        </NodeOutcomeVariable>
                        <NodeOutcomeValue>FAILURE</NodeOutcomeValue>
                    </EQInternal>|],
              "isOutcomeFailure?('TestVars1)")
            ,("SUCCESS",
              [r|   <EQInternal>
                        <NodeOutcomeValue>success</NodeOutcomeValue>
                        <NodeOutcomeVariable>
                            <NodeRef dir="child">TestVars2</NodeRef>
                        </NodeOutcomeVariable>
                    </EQInternal>|],
              "isOutcome?('TestVars2,success)")
            ,("SKIPPED",
              [r|   <EQInternal>
                        <NodeOutcomeVariable>
                            <NodeRef dir="child">TestVars1</NodeRef>
                        </NodeOutcomeVariable>
                        <NodeOutcomeValue>SKiPPED</NodeOutcomeValue>
                    </EQInternal>|],
              "isOutcome?('TestVars1,skipped)")
            ,("INTERRUPTED",
              [r|   <EQInternal>
                        <NodeOutcomeVariable>
                            <NodeRef dir="child">TestVars1</NodeRef>
                        </NodeOutcomeVariable>
                        <NodeOutcomeValue>INTERRUPTED</NodeOutcomeValue>
                    </EQInternal>|],
              "isOutcome?('TestVars1,interrupted)")
            ]

testsPrettyStateEq :: TestTree
testsPrettyStateEq =
  testGroup
    "Node State Equality" $
        map (testify'' elementVisitor)
            [("FINISHED",
              [r|   <EQInternal>
                        <NodeStateVariable>
                            <NodeRef dir="child">TestVars1</NodeRef>
                        </NodeStateVariable>
                        <NodeStateValue>FINISHED</NodeStateValue>
                    </EQInternal>|],
              "isStatus?('TestVars1,finished)")
            ,("WAITING",
              [r|   <EQInternal>
                        <NodeStateVariable>
                            <NodeRef dir="child">TestVars1</NodeRef>
                        </NodeStateVariable>
                        <NodeStateValue>waiting</NodeStateValue>
                    </EQInternal>|],
              "isStatus?('TestVars1,waiting)")
            ,("EXECUTING",
              [r|   <EQInternal>
                        <NodeStateVariable>
                            <NodeRef dir="child">TestVars1</NodeRef>
                        </NodeStateVariable>
                        <NodeStateValue>ExEcUTING</NodeStateValue>
                    </EQInternal>|],
              "isStatus?('TestVars1,executing)")
            ,("FINISHING",
              [r|   <EQInternal>
                        <NodeStateValue>FINISHING</NodeStateValue>
                        <NodeStateVariable>
                            <NodeRef dir="child">TestVars1</NodeRef>
                        </NodeStateVariable>
                    </EQInternal>|],
              "isStatus?('TestVars1,finishing)")
            ,("FAILING",
              [r|   <EQInternal>
                        <NodeStateVariable>
                            <NodeRef dir="child">TestVars1</NodeRef>
                        </NodeStateVariable>
                        <NodeStateValue>Failing</NodeStateValue>
                    </EQInternal>|],
              "isStatus?('TestVars1,failing)")
            ,("ITERATION_ENDED",
              [r|   <EQInternal>
                        <NodeStateVariable>
                            <NodeRef dir="child">TestVars1</NodeRef>
                        </NodeStateVariable>
                        <NodeStateValue>ITERATION_ENDED</NodeStateValue>
                    </EQInternal>|],
              "isStatus?('TestVars1,iterationEnded)")
            ,("INACTIVE",
              [r|   <EQInternal>
                        <NodeStateVariable>
                            <NodeRef dir="child">TestVars1</NodeRef>
                        </NodeStateVariable>
                        <NodeStateValue>INACTIVE</NodeStateValue>
                    </EQInternal>|],
              "isStatus?('TestVars1,inactive)")
            ]


testsBinarizeList :: TestTree
testsBinarizeList =
  testGroup
    "Binarize a list" $
        map (\(msg,i,o) -> testCase msg $ binarizeList i @?= o)
            [("[]",[] :: [Int],Nothing)
            ,("[1]",[1],Just $ Root 1)
            ,("[1,2]",[1,2],Just $ Branches (Root 1) (Root 2))
            ,("[1,2,3]",[1,2,3],
                Just $
                    Branches
                        (Branches (Root 1) (Root 2))
                        (Root 3)
             )
            ,("[1,2,3,4]",[1,2,3,4],
                Just $
                    Branches
                        (Branches (Root 1) (Root 2))
                        (Branches (Root 3) (Root 4))
             )
            ,("[1,2,3,4,5]",[1,2,3,4,5],
                Just $
                    Branches
                        (Branches (Root 1) (Root 2))
                        (Branches
                            (Branches (Root 3) (Root 4))
                            (Root 5))
             )
            ,("[1,2,3,4,5,6]",[1,2,3,4,5,6],
                Just $
                    Branches
                        (Branches (Root 1) (Root 2))
                        (Branches
                            (Branches (Root 3) (Root 4))
                            (Branches (Root 5) (Root 6)))

             )
            ,("[1,2,3,4,5,6,7]",[1,2,3,4,5,6,7],
                Just $
                    Branches
                        (Branches (Root 1) (Root 2))
                        (Branches
                            (Branches (Root 3) (Root 4))
                            (Branches
                                (Branches (Root 5) (Root 6))
                                (Root 7)))

             )
            ]


testsParseNodeCondition :: TestTree
testsParseNodeCondition =
    testGroup "Parse a node condition" $
        map (testify'' elementVisitor)
            [("StartCondition",
              [r|
              <StartCondition>
                <EQInternal>
                    <NodeStateVariable>
                        <NodeRef dir="sibling">TestVars1</NodeRef>
                    </NodeStateVariable>
                    <NodeStateValue>FINISHED</NodeStateValue>
                </EQInternal>
              </StartCondition>|],
              "(startc: (isStatus?('TestVars1,finished)))")
            ,("RepeatCondition",
              [r|
              <RepeatCondition>
                <BooleanVariable>Variable1</BooleanVariable>
              </RepeatCondition>|],
              "(repeatc: (var('Variable1)))")
            ,("PreCondition",
              [r|
              <PreCondition>
                <BooleanValue>TRUE</BooleanValue>
              </PreCondition>|],
              "(pre: (const(val(true))))")
            ,("PostCondition",
              [r|
              <PostCondition>
                <BooleanValue>FaLSE</BooleanValue>
              </PostCondition>|],
              "(post: (const(val(false))))")
            ,("InvariantCondition",
              [r|
              <InvariantCondition>
                <BooleanValue>TRUE</BooleanValue>
              </InvariantCondition>|],
              "(inv: (const(val(true))))")
            ,("InvariantCondition2",
              [r|
              <InvariantCondition>
                <NoChildFailed>
                  <NodeRef dir="self"/>
                </NoChildFailed>
              </InvariantCondition>|],
              "(inv: (noChildFailed))")
            ,("EndCondition",
              [r|
              <EndCondition>
                <BooleanValue>TRUE</BooleanValue>
              </EndCondition>|],
              "(endc: (const(val(true))))")
            ,("ExitCondition",
              [r|
              <ExitCondition>
                <BooleanValue>TRUE</BooleanValue>
              </ExitCondition>|],
              "(exitc: (const(val(true))))")
            ,("SkipCondition",
              [r|
              <SkipCondition>
                <BooleanValue>TRUE</BooleanValue>
              </SkipCondition>|],
              "(skip: (const(val(true))))")
            ]


testLookups :: TestTree
testLookups =
  testGroup "Lookups" $
    map (testify'' elementVisitor)
      [("LookupOnChange wo args",
        [r|
        <LookupOnChange epx="Lookup"><Name><StringValue>inConflict</StringValue></Name></LookupOnChange>
        |],
        "lookupOnChange('inConflict, (nilarg), val(0.0))")
      ,("LookupOnChange 1 arg",
        [r|
        <LookupOnChange>
            <Name>
                <StringValue>A</StringValue>
            </Name>
            <Arguments ColNo="23" LineNo="15">
                <IntegerValue>1</IntegerValue>
            </Arguments>
        </LookupOnChange>
        |],
        [r|lookupOnChange('A, (val(1)), val(0.0))|])
      ,("LookupOnChange 2 arg",
        [r|
        <LookupOnChange>
            <Name>
                <StringValue>A</StringValue>
            </Name>
            <Arguments ColNo="23" LineNo="15">
                <StringValue>is</StringValue>
                <StringValue>isnot</StringValue>
            </Arguments>
        </LookupOnChange>
        |],
        [r|lookupOnChange('A,(val("is") val("isnot")), val(0.0))|])
      ,("LookupOnChange tolerance",
        [r|
        <LookupOnChange>
            <Name>
                <StringValue>A</StringValue>
            </Name>
            <Tolerance>
                <IntegerValue>1</IntegerValue>
            </Tolerance>
            <Arguments ColNo="23" LineNo="15">
                <StringValue>is</StringValue>
            </Arguments>
        </LookupOnChange>
        |],
        [r|lookupOnChange('A,(val("is")), val(1))|])
        ,("LookupOnChange 2 arg + tolerance",
        [r|
        <LookupOnChange>
            <Name>
                <StringValue>A</StringValue>
            </Name>
            <Tolerance>
                <IntegerValue>1</IntegerValue>
            </Tolerance>
            <Arguments ColNo="23" LineNo="15">
                <StringValue>is</StringValue>
                <StringValue>isnot</StringValue>
            </Arguments>
        </LookupOnChange>
        |],
        [r|lookupOnChange('A, (val("is") val("isnot")) , val(1))|])
        ,("LookupOnChange name+tolerance, no args",
        [r|
        <LookupOnChange>
            <Name>
                <StringValue>time</StringValue>
            </Name>
            <Tolerance>
                <RealValue>0.1</RealValue>
            </Tolerance>
        </LookupOnChange>
        |],
        [r|lookupOnChange('time,(nilarg),val (0.1))|])
      ]

testArithmeticExpressions :: TestTree
testArithmeticExpressions =
  testGroup "ArithmeticOperator" $
    map (testify'' elementVisitor)
    [ ("ADD",
       [r|
        <ADD ColNo="14" LineNo="4">
          <IntegerValue>0</IntegerValue>
          <IntegerValue>1</IntegerValue>
        </ADD>
        |],
       "_+_(const(val(0)),const(val(1)))")
    , ("SUB",
       [r|
        <SUB ColNo="14" LineNo="4">
          <IntegerValue>0</IntegerValue>
          <IntegerValue>1</IntegerValue>
        </SUB>
        |],
       "_-_(const(val(0)),const(val(1)))")
    , ("MUL",
       [r|
        <MUL ColNo="14" LineNo="4">
          <IntegerValue>0</IntegerValue>
          <IntegerValue>1</IntegerValue>
        </MUL>
        |],
       "_*_(const(val(0)),const(val(1)))")
    , ("DIV",
       [r|
        <DIV ColNo="14" LineNo="4">
          <IntegerValue>0</IntegerValue>
          <IntegerValue>1</IntegerValue>
        </DIV>
        |],
       "_/_(const(val(0)),const(val(1)))")
    , ("MOD",
       [r|
        <MOD ColNo="14" LineNo="4">
          <IntegerValue>8</IntegerValue>
          <IntegerValue>3</IntegerValue>
        </MOD>
        |],
       "_rem_(const(val(8)),const(val(3)))")
    , ("MAX",
       [r|
        <MAX ColNo="14" LineNo="4">
          <IntegerValue>0</IntegerValue>
          <IntegerValue>1</IntegerValue>
        </MAX>
        |],
       "_max_(const(val(0)),const(val(1)))")
    , ("MIN",
       [r|
        <MIN ColNo="14" LineNo="4">
          <IntegerValue>0</IntegerValue>
          <IntegerValue>1</IntegerValue>
        </MIN>
        |],
       "_min_(const(val(0)),const(val(1)))")
    , ("SQRT",
       [r|
        <SQRT ColNo="14" LineNo="4">
          <IntegerValue>9</IntegerValue>
        </SQRT>
        |],
       "(func(sqrt,const(val(9))))")
    , ("ABS",
       [r|
        <ABS ColNo="14" LineNo="4">
          <IntegerValue>0</IntegerValue>
        </ABS>
        |],
       "(func(absp,const(val(0))))")
    , ("CEIL",
       [r|
        <CEIL ColNo="14" LineNo="4">
          <RealValue>4.7</RealValue>
        </CEIL>
        |],
       "(func(ceiling,const(val(4.7))))")
    , ("FLOOR",
       [r|
        <FLOOR ColNo="14" LineNo="4">
          <RealValue>4.7</RealValue>
        </FLOOR>
        |],
       "(func(floor,const(val(4.7))))")
    ]

testUpdate :: TestTree
testUpdate =
  testGroup "Update" $
    map (testify'' elementVisitor)
    [ ("Update",
       [r|
        <Update>
          <Pair>
            <Name>taskId</Name>
            <IntegerVariable>waypt_id</IntegerVariable>
          </Pair>
          <Pair>
            <Name>result</Name>
            <IntegerVariable>cmd_return_val</IntegerVariable>
          </Pair>
        </Update>
        |],
       "(< 'taskId ; var('waypt_id) > < 'result ; var('cmd_return_val) >)")
    , ("Update2",
        [r|
          <Update>
            <Pair>
              <Name>lookup</Name>
              <LookupNow>
                <Name>
                  <StringValue>someValue</StringValue>
                </Name>
              </LookupNow>
            </Pair>
          </Update>
          |],
        "(< 'lookup ; lookup ('someValue, (nilarg)) >)")
    , ("UpdateVariable",
        [r|
          <Update>
            <Pair>
              <Name>realconstant</Name>
              <RealValue>3.141</RealValue>
            </Pair>
            <Pair>
              <Name>val</Name>
              <ArrayVariable>src</ArrayVariable>
            </Pair>
          </Update>
        |],
        "(< 'realconstant ; const(val(3.141)) > < 'val ; arrayVar('src) >)")

    ]