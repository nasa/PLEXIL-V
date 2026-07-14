{-# LANGUAGE QuasiQuotes #-}

module PLEXIL.DebugLogParserSpec where

import Data.Either (isLeft, isRight)
import qualified Data.Set as Set
import PLEXIL.DebugLogParser
import PLEXIL.Trace
import Test.Hspec
import Text.Parsec (parse)
import Text.RawString.QQ

spec :: Spec
spec = do
  describe "parseTrace" $ do
    it "should parse PLEXIL v6 an empty macro" $
      let logEntry =
            [r|[PlexilExec:step] ==>Start cycle 3
[PlexilExec:step] ==>End cycle 3
|]
       in parseTrace logEntry
            `shouldBe` Right (Trace [Macro []])

    it "should parse two PLEXIL v6 macros" $
      let logEntry =
            [r|[PlexilExec:step] ==>Start cycle 1
[PlexilExec:step] ==>End cycle 1
[PlexilExec:step] ==>Start cycle 2
[PlexilExec:step][2:0:0] Transitioning Assignment node GetResolutionType 0x12fe04d40 from EXECUTING to ITERATION_ENDED
[PlexilExec:step][2:1:0] Transitioning Assignment node GetResolutionType 0x12fe04d40 from ITERATION_ENDED to FINISHED
[PlexilExec:step][2:2:0] Transitioning Command node SpeedResolution 0x12fe04e90 from WAITING to FINISHED
[PlexilExec:step][2:3:0] Transitioning Command node AltitudeResolution 0x12fe05130 from WAITING to FINISHED
[PlexilExec:step][2:4:0] Transitioning Command node TrackResolution 0x12fe053d0 from WAITING to FINISHED
[PlexilExec:step][2:5:0] Transitioning Command node VerticalSpeedResolution 0x12fe05670 from WAITING to FINISHED
[PlexilExec:step][2:6:0] Transitioning NodeList node TrafficConflictHandler 0x12fe04b50 from EXECUTING to FINISHING
[PlexilExec:step][2:7:0] Transitioning NodeList node TrafficConflictHandler 0x12fe04b50 from FINISHING to ITERATION_ENDED
[PlexilExec:step][2:8:0] Transitioning NodeList node TrafficConflictHandler 0x12fe04b50 from ITERATION_ENDED to FINISHED
[PlexilExec:step] ==>End cycle 2
[PlexilExec:step] ==>Start cycle 3
[PlexilExec:step] ==>End cycle 3
|]
       in parseTrace logEntry
            `shouldBe` Right
              ( Trace
                  [ Macro [],
                    Macro
                      [ Micro $ Set.fromList [Transition (Id "'GetResolutionType") Executing IterationEnded],
                        Micro $ Set.fromList [Transition (Id "'GetResolutionType") IterationEnded Finished],
                        Micro $ Set.fromList [Transition (Id "'SpeedResolution") Waiting Finished],
                        Micro $ Set.fromList [Transition (Id "'AltitudeResolution") Waiting Finished],
                        Micro $ Set.fromList [Transition (Id "'TrackResolution") Waiting Finished],
                        Micro $ Set.fromList [Transition (Id "'VerticalSpeedResolution") Waiting Finished],
                        Micro $ Set.fromList [Transition (Id "'TrafficConflictHandler") Executing Finishing],
                        Micro $ Set.fromList [Transition (Id "'TrafficConflictHandler") Finishing IterationEnded],
                        Micro $ Set.fromList [Transition (Id "'TrafficConflictHandler") IterationEnded Finished]
                      ],
                    Macro []
                  ]
              )

  describe "parseMacro" $ do
    it "should parse PLEXIL v6 macro entries" $
      let logEntry =
            [r|[PlexilExec:step] ==>Start cycle 3
[PlexilExec:step][3:0:0] Transitioning Command node commandabort1 0x139704910 from FAILING to ITERATION_ENDED
[PlexilExec:step][3:0:1] Transitioning Command node commandabort2 0x139704910 from FAILING to ITERATION_ENDED
[PlexilExec:step][3:1:0] Transitioning Command node commandabort1 0x139704910 from ITERATION_ENDED to FINISHED
[PlexilExec:step] ==>End cycle 3
|]
       in parseMacro logEntry
            `shouldBe` Right
              ( Macro
                  [ Micro $
                      Set.fromList
                        [ Transition (Id "'commandabort1") Failing IterationEnded,
                          Transition (Id "'commandabort2") Failing IterationEnded
                        ],
                    Micro $ Set.fromList [Transition (Id "'commandabort1") IterationEnded Finished]
                  ]
              )

    it "should parse a complex PLEXIL v6 macro entries" $
      let logEntry =
            [r|[PlexilExec:step] ==>Start cycle 1
[PlexilExec:step][1:0:0] Transitioning NodeList node TrafficConflictHandler 0x12fe04b50 from INACTIVE to WAITING
[PlexilExec:step][1:1:0] Transitioning NodeList node TrafficConflictHandler 0x12fe04b50 from WAITING to EXECUTING
[PlexilExec:step][1:2:0] Transitioning Assignment node GetResolutionType 0x12fe04d40 from INACTIVE to WAITING
[PlexilExec:step][1:2:1] Transitioning Command node SpeedResolution 0x12fe04e90 from INACTIVE to WAITING
[PlexilExec:step][1:2:2] Transitioning Command node AltitudeResolution 0x12fe05130 from INACTIVE to WAITING
[PlexilExec:step][1:2:3] Transitioning Command node TrackResolution 0x12fe053d0 from INACTIVE to WAITING
[PlexilExec:step][1:2:4] Transitioning Command node VerticalSpeedResolution 0x12fe05670 from INACTIVE to WAITING
[PlexilExec:step][1:3:0] Transitioning Assignment node GetResolutionType 0x12fe04d40 from WAITING to EXECUTING
[PlexilExec:step] ==>End cycle 1
|]
       in parseMacro logEntry
            `shouldBe` Right
              ( Macro
                  [ Micro $ Set.fromList [Transition (Id "'TrafficConflictHandler") Inactive Waiting],
                    Micro $ Set.fromList [Transition (Id "'TrafficConflictHandler") Waiting Executing],
                    Micro $
                      Set.fromList
                        [ Transition (Id "'GetResolutionType") Inactive Waiting,
                          Transition (Id "'SpeedResolution") Inactive Waiting,
                          Transition (Id "'AltitudeResolution") Inactive Waiting,
                          Transition (Id "'TrackResolution") Inactive Waiting,
                          Transition (Id "'VerticalSpeedResolution") Inactive Waiting
                        ],
                    Micro $ Set.fromList [Transition (Id "'GetResolutionType") Waiting Executing]
                  ]
              )

  describe "parseMicro" $ do
    it "should parse a PLEXIL v4 entry" $
      let logEntry = "[PlexilExec:step][1:0:0] Transitioning node TRAFFIC_RESOLUTION 0x6e3dc0 from INACTIVE to WAITING\n"
       in parseMicro logEntry `shouldBe` Right (Micro $ Set.fromList [Transition (Id "'TRAFFIC_RESOLUTION") Inactive Waiting])

    it "should parse many PLEXIL v4 entries" $
      let logEntry =
            [r|[PlexilExec:step][1:0:0] Transitioning node TRAFFIC_RESOLUTION 0x6e3dc0 from INACTIVE to WAITING
[PlexilExec:step][1:0:0] Transitioning node Example7 0x19c3370 from INACTIVE to WAITING
|]
       in parseMicro logEntry
            `shouldBe` Right
              ( Micro $
                  Set.fromList
                    [ Transition (Id "'TRAFFIC_RESOLUTION") Inactive Waiting,
                      Transition (Id "'Example7") Inactive Waiting
                    ]
              )

    it "should group transitions of the same identified micro step" $
      let logEntry =
            [r|[PlexilExec:step][1:0:0] Transitioning node TRAFFIC_RESOLUTION 0x6e3dc0 from INACTIVE to WAITING
[PlexilExec:step][1:1:0] Transitioning node Example7 0x19c3370 from INACTIVE to WAITING
|]
       in parseMicro logEntry
            `shouldBe` Right (Micro $ Set.fromList [Transition (Id "'TRAFFIC_RESOLUTION") Inactive Waiting])

    it "should parse a PLEXIL v6 entry" $
      let logEntry = "[PlexilExec:step][1:0:0] Transitioning Command node commandabort1 0x139704910 from INACTIVE to WAITING\n"
       in parseMicro logEntry `shouldBe` Right (Micro $ Set.fromList [Transition (Id "'commandabort1") Inactive Waiting])

    it "should parse many PLEXIL v6 entries" $
      let logEntry =
            [r|[PlexilExec:step][1:2:0] Transitioning Assignment node GetResolutionType 0x12fe04d40 from INACTIVE to WAITING
[PlexilExec:step][1:2:1] Transitioning Command node SpeedResolution 0x12fe04e90 from INACTIVE to WAITING
|]
       in parseMicro logEntry
            `shouldBe` Right
              ( Micro $
                  Set.fromList
                    [ Transition (Id "'GetResolutionType") Inactive Waiting,
                      Transition (Id "'SpeedResolution") Inactive Waiting
                    ]
              )

  describe "transitionParserWithId" $ do
    it "should parse a log entry that has a compatible micro step identifier" $
      let logEntry = "[PlexilExec:step][1:0:1] Transitioning node TRAFFIC_RESOLUTION 0x6e3dc0 from INACTIVE to WAITING\n"
       in parse (transitionParserWithId [1, 0]) "transition" logEntry `shouldBe` (Right ([1, 0, 1], Transition (Id "'TRAFFIC_RESOLUTION") Inactive Waiting))

    it "should not parse a log entry that has an incompatible micro step identifier" $
      let logEntry = "[PlexilExec:step][1:0:1] Transitioning node TRAFFIC_RESOLUTION 0x6e3dc0 from INACTIVE to WAITING\n"
       in parse (transitionParserWithId [1, 1]) "transition" logEntry `shouldSatisfy` isLeft

    it "should parse a log entry if the micro step identifier is empty" $
      let logEntry = "[PlexilExec:step][1:0:1] Transitioning node TRAFFIC_RESOLUTION 0x6e3dc0 from INACTIVE to WAITING\n"
       in parse (transitionParserWithId []) "transition" logEntry `shouldSatisfy` isRight

  describe "parseTransition" $ do
    it "should parse a PLEXIL v4 entry" $
      let logEntry = "[PlexilExec:step][1:0:0] Transitioning node TRAFFIC_RESOLUTION 0x6e3dc0 from INACTIVE to WAITING\n"
       in parseTransition logEntry `shouldBe` (Right $ Transition (Id "'TRAFFIC_RESOLUTION") Inactive Waiting)

    it "should parse a PLEXIL v6 entry" $
      let logEntry = "[PlexilExec:step][1:0:0] Transitioning Command node commandabort1 0x139704910 from INACTIVE to WAITING\n"
       in parseTransition logEntry `shouldBe` Right (Transition (Id "'commandabort1") Inactive Waiting)

    it "battery of PLEXIL v4 tests" $
      let logEntries =
            [ "[PlexilExec:step][1:0:0] Transitioning node Example7 0x19c3370 from INACTIVE to WAITING\n",
              "[PlexilExec:step][1:0:0] Transitioning node Example7 0x19c3370 from WAITING to EXECUTING\n",
              "[PlexilExec:step][1:0:0] Transitioning node TRAFFIC_RESOLUTION 0x6e3dc0 from INACTIVE to WAITING\n"
            ]
       in map parseTransition logEntries
            `shouldBe` [ Right $ Transition (Id "'Example7") Inactive Waiting,
                         Right $ Transition (Id "'Example7") Waiting Executing,
                         Right $ Transition (Id "'TRAFFIC_RESOLUTION") Inactive Waiting
                       ]

  describe "isKeyEntry" $ do
    it "should accept a 'Transitioning node' entry" $
      isKeyEntry "[PlexilExec:step][1:0:0] Transitioning node TRAFFIC_RESOLUTION 0x6e3dc0 from INACTIVE to WAITING"
        `shouldBe` True
    it "should accept a 'Transitioning <node-type> node' entry" $
      isKeyEntry "[PlexilExec:step][1:0:0] Transitioning Command node commandabort1 0x139704910 from INACTIVE to WAITING"
        `shouldBe` True
    it "should reject an entry with only the header" $
      isKeyEntry "[PlexilExec:step]"
        `shouldBe` False
    it "should reject an entry with the header surrounded by other text" $
      isKeyEntry "Other text [PlexilExec:step][1:0:0] Transitioning node TRAFFIC_RESOLUTION 0x6e3dc0 from INACTIVE to WAITING"
        `shouldBe` False
    it "should accept a 'Start cycle' entry" $
      isKeyEntry "[PlexilExec:step] ==>Start cycle 1"
        `shouldBe` True
    it "should accept an 'End cycle' entry" $
      isKeyEntry "[PlexilExec:step] ==>End cycle 1"
        `shouldBe` True

  describe "filterEntries" $ do
    it "should filter only key entries" $
      filterEntries
        [r|[PlexilExec:step] ==>Start cycle 1
[PlexilExec:step][1:0] Check queue: commandabort1
[PlexilExec:step] Node commandabort1 0x139704910 can transition from INACTIVE to WAITING
[PlexilExec:step] adding commandabort1 0x139704910 to state change queue
[PlexilExec:step][1:0] State change queue: commandabort1
[PlexilExec:step][1:0:0] Transitioning Command node commandabort1 0x139704910 from INACTIVE to WAITING
[PlexilExec:step][1:1] Check queue: commandabort1
[PlexilExec:step] Node commandabort1 0x139704910 can transition from WAITING to EXECUTING
[PlexilExec:step] adding commandabort1 0x139704910 to state change queue
[PlexilExec:step][1:1] State change queue: commandabort1
[PlexilExec:step][1:1:0] Transitioning Command node commandabort1 0x139704910 from WAITING to EXECUTING
[PlexilExec:step] ==>End cycle 1
|]
        `shouldBe` [r|[PlexilExec:step] ==>Start cycle 1
[PlexilExec:step][1:0:0] Transitioning Command node commandabort1 0x139704910 from INACTIVE to WAITING
[PlexilExec:step][1:1:0] Transitioning Command node commandabort1 0x139704910 from WAITING to EXECUTING
[PlexilExec:step] ==>End cycle 1
|]
    it "should filter cycle-tagged start cycle entries" $
      filterEntries
        [r|[PlexilExec:cycle] ==>Start cycle 1
[PlexilExec:cycle] ==>End cycle 1
|]
        `shouldBe` [r|[PlexilExec:cycle] ==>Start cycle 1
[PlexilExec:cycle] ==>End cycle 1
|]

  describe "filterAndParseTrace" $ do
    it "should correctly process a full file" $
      let logEntry =
            [r|

Running executive from /Users/mfeliuga/Desktop/projects/sws/plexil/rwl-semantics/plexil5@gitlab/plexil
  Plan:           /Users/mfeliuga/Desktop/projects/sws/plexil/rwl-semantics/plexil5@gitlab/semantics/benchmark/icarous/cognition/TrafficConflictHandler.plx
  Resource:       resource.data
  Script:         input.psx

[PlexilExec:step] ==>Start cycle 1
[PlexilExec:step][1:0] Check queue: TrafficConflictHandler
[PlexilExec:step] Node TrafficConflictHandler 0x12fe04b50 can transition from INACTIVE to WAITING
[PlexilExec:step] adding TrafficConflictHandler 0x12fe04b50 to state change queue
[PlexilExec:step][1:0] State change queue: TrafficConflictHandler
[PlexilExec:step][1:0:0] Transitioning NodeList node TrafficConflictHandler 0x12fe04b50 from INACTIVE to WAITING
[PlexilExec:step][1:1] Check queue: TrafficConflictHandler
[PlexilExec:step] Node TrafficConflictHandler 0x12fe04b50 can transition from WAITING to EXECUTING
[PlexilExec:step] adding TrafficConflictHandler 0x12fe04b50 to state change queue
[PlexilExec:step][1:1] State change queue: TrafficConflictHandler
[PlexilExec:step][1:1:0] Transitioning NodeList node TrafficConflictHandler 0x12fe04b50 from WAITING to EXECUTING
[PlexilExec:step][1:2] Check queue: TrafficConflictHandler GetResolutionType SpeedResolution AltitudeResolution TrackResolution VerticalSpeedResolution
[PlexilExec:step] Node GetResolutionType 0x12fe04d40 can transition from INACTIVE to WAITING
[PlexilExec:step] adding GetResolutionType 0x12fe04d40 to state change queue
[PlexilExec:step] Node SpeedResolution 0x12fe04e90 can transition from INACTIVE to WAITING
[PlexilExec:step] adding SpeedResolution 0x12fe04e90 to state change queue
[PlexilExec:step] Node AltitudeResolution 0x12fe05130 can transition from INACTIVE to WAITING
[PlexilExec:step] adding AltitudeResolution 0x12fe05130 to state change queue
[PlexilExec:step] Node TrackResolution 0x12fe053d0 can transition from INACTIVE to WAITING
[PlexilExec:step] adding TrackResolution 0x12fe053d0 to state change queue
[PlexilExec:step] Node VerticalSpeedResolution 0x12fe05670 can transition from INACTIVE to WAITING
[PlexilExec:step] adding VerticalSpeedResolution 0x12fe05670 to state change queue
[PlexilExec:step][1:2] State change queue: GetResolutionType SpeedResolution AltitudeResolution TrackResolution VerticalSpeedResolution
[PlexilExec:step][1:2:0] Transitioning Assignment node GetResolutionType 0x12fe04d40 from INACTIVE to WAITING
[PlexilExec:step][1:2:1] Transitioning Command node SpeedResolution 0x12fe04e90 from INACTIVE to WAITING
[PlexilExec:step][1:2:2] Transitioning Command node AltitudeResolution 0x12fe05130 from INACTIVE to WAITING
[PlexilExec:step][1:2:3] Transitioning Command node TrackResolution 0x12fe053d0 from INACTIVE to WAITING
[PlexilExec:step][1:2:4] Transitioning Command node VerticalSpeedResolution 0x12fe05670 from INACTIVE to WAITING
[PlexilExec:step][1:3] Check queue: GetResolutionType TrafficConflictHandler SpeedResolution AltitudeResolution TrackResolution VerticalSpeedResolution
[PlexilExec:step] Node GetResolutionType 0x12fe04d40 can transition from WAITING to EXECUTING
[PlexilExec:step] adding GetResolutionType 0x12fe04d40 to pending queue
[PlexilExec:step][1:3] Pending queue: GetResolutionType
[PlexilExec:step] processing resource reservations at priority 100000
[PlexilExec:step] 1 nodes eligible to acquire resources
[PlexilExec:step] adding GetResolutionType 0x12fe04d40 to state change queue
[PlexilExec:step][1:3] State change queue: GetResolutionType
[PlexilExec:step][1:3:0] Transitioning Assignment node GetResolutionType 0x12fe04d40 from WAITING to EXECUTING
[PlexilExec:step] ==>End cycle 1
[PlexilExec:step] ==>Start cycle 2
[PlexilExec:step][2:0] Check queue: GetResolutionType TrafficConflictHandler SpeedResolution AltitudeResolution TrackResolution VerticalSpeedResolution
[PlexilExec:step] Node GetResolutionType 0x12fe04d40 can transition from EXECUTING to ITERATION_ENDED
[PlexilExec:step] adding GetResolutionType 0x12fe04d40 to state change queue
[PlexilExec:step][2:0] State change queue: GetResolutionType
[PlexilExec:step][2:0:0] Transitioning Assignment node GetResolutionType 0x12fe04d40 from EXECUTING to ITERATION_ENDED
[PlexilExec:step][2:1] Check queue: GetResolutionType TrafficConflictHandler SpeedResolution AltitudeResolution TrackResolution VerticalSpeedResolution
[PlexilExec:step] Node GetResolutionType 0x12fe04d40 can transition from ITERATION_ENDED to FINISHED
[PlexilExec:step] adding GetResolutionType 0x12fe04d40 to state change queue
[PlexilExec:step][2:1] State change queue: GetResolutionType
[PlexilExec:step][2:1:0] Transitioning Assignment node GetResolutionType 0x12fe04d40 from ITERATION_ENDED to FINISHED
[PlexilExec:step][2:2] Check queue: GetResolutionType TrafficConflictHandler SpeedResolution AltitudeResolution TrackResolution VerticalSpeedResolution
[PlexilExec:step] Node SpeedResolution 0x12fe04e90 can transition from WAITING to FINISHED
[PlexilExec:step] adding SpeedResolution 0x12fe04e90 to state change queue
[PlexilExec:step][2:2] State change queue: SpeedResolution
[PlexilExec:step][2:2:0] Transitioning Command node SpeedResolution 0x12fe04e90 from WAITING to FINISHED
[PlexilExec:step][2:3] Check queue: SpeedResolution TrafficConflictHandler GetResolutionType AltitudeResolution TrackResolution VerticalSpeedResolution
[PlexilExec:step] Node AltitudeResolution 0x12fe05130 can transition from WAITING to FINISHED
[PlexilExec:step] adding AltitudeResolution 0x12fe05130 to state change queue
[PlexilExec:step][2:3] State change queue: AltitudeResolution
[PlexilExec:step][2:3:0] Transitioning Command node AltitudeResolution 0x12fe05130 from WAITING to FINISHED
[PlexilExec:step][2:4] Check queue: AltitudeResolution TrafficConflictHandler GetResolutionType SpeedResolution TrackResolution VerticalSpeedResolution
[PlexilExec:step] Node TrackResolution 0x12fe053d0 can transition from WAITING to FINISHED
[PlexilExec:step] adding TrackResolution 0x12fe053d0 to state change queue
[PlexilExec:step][2:4] State change queue: TrackResolution
[PlexilExec:step][2:4:0] Transitioning Command node TrackResolution 0x12fe053d0 from WAITING to FINISHED
[PlexilExec:step][2:5] Check queue: TrackResolution TrafficConflictHandler GetResolutionType SpeedResolution AltitudeResolution VerticalSpeedResolution
[PlexilExec:step] Node VerticalSpeedResolution 0x12fe05670 can transition from WAITING to FINISHED
[PlexilExec:step] adding VerticalSpeedResolution 0x12fe05670 to state change queue
[PlexilExec:step][2:5] State change queue: VerticalSpeedResolution
[PlexilExec:step][2:5:0] Transitioning Command node VerticalSpeedResolution 0x12fe05670 from WAITING to FINISHED
[PlexilExec:step][2:6] Check queue: VerticalSpeedResolution TrafficConflictHandler GetResolutionType SpeedResolution AltitudeResolution TrackResolution
[PlexilExec:step] Node TrafficConflictHandler 0x12fe04b50 can transition from EXECUTING to FINISHING
[PlexilExec:step] adding TrafficConflictHandler 0x12fe04b50 to state change queue
[PlexilExec:step][2:6] State change queue: TrafficConflictHandler
[PlexilExec:step][2:6:0] Transitioning NodeList node TrafficConflictHandler 0x12fe04b50 from EXECUTING to FINISHING
[PlexilExec:step][2:7] Check queue: TrafficConflictHandler
[PlexilExec:step] Node TrafficConflictHandler 0x12fe04b50 can transition from FINISHING to ITERATION_ENDED
[PlexilExec:step] adding TrafficConflictHandler 0x12fe04b50 to state change queue
[PlexilExec:step][2:7] State change queue: TrafficConflictHandler
[PlexilExec:step][2:7:0] Transitioning NodeList node TrafficConflictHandler 0x12fe04b50 from FINISHING to ITERATION_ENDED
[PlexilExec:step][2:8] Check queue: TrafficConflictHandler
[PlexilExec:step] Node TrafficConflictHandler 0x12fe04b50 can transition from ITERATION_ENDED to FINISHED
[PlexilExec:step] adding TrafficConflictHandler 0x12fe04b50 to state change queue
[PlexilExec:step][2:8] State change queue: TrafficConflictHandler
[PlexilExec:step][2:8:0] Transitioning NodeList node TrafficConflictHandler 0x12fe04b50 from ITERATION_ENDED to FINISHED
[PlexilExec:step] Marking TrafficConflictHandler 0x12fe04b50 as a finished root node
[PlexilExec:step] ==>End cycle 2
[PlexilExec:step] ==>Start cycle 3
[PlexilExec:step][3:0] Check queue:
[PlexilExec:step] ==>End cycle 3
[PlexilExec:step] ==>Start cycle 4
[PlexilExec:step][4:0] Check queue:
[PlexilExec:step] ==>End cycle 4
|]
       in filterAndParseTrace logEntry
            `shouldBe` Right
              ( Trace
                  [ Macro
                      [ Micro $ Set.fromList [Transition (Id "'TrafficConflictHandler") Inactive Waiting],
                        Micro $ Set.fromList [Transition (Id "'TrafficConflictHandler") Waiting Executing],
                        Micro $
                          Set.fromList
                            [ Transition (Id "'GetResolutionType") Inactive Waiting,
                              Transition (Id "'SpeedResolution") Inactive Waiting,
                              Transition (Id "'AltitudeResolution") Inactive Waiting,
                              Transition (Id "'TrackResolution") Inactive Waiting,
                              Transition (Id "'VerticalSpeedResolution") Inactive Waiting
                            ],
                        Micro $ Set.fromList [Transition (Id "'GetResolutionType") Waiting Executing]
                      ],
                    Macro
                      [ Micro $ Set.fromList [Transition (Id "'GetResolutionType") Executing IterationEnded],
                        Micro $ Set.fromList [Transition (Id "'GetResolutionType") IterationEnded Finished],
                        Micro $ Set.fromList [Transition (Id "'SpeedResolution") Waiting Finished],
                        Micro $ Set.fromList [Transition (Id "'AltitudeResolution") Waiting Finished],
                        Micro $ Set.fromList [Transition (Id "'TrackResolution") Waiting Finished],
                        Micro $ Set.fromList [Transition (Id "'VerticalSpeedResolution") Waiting Finished],
                        Micro $ Set.fromList [Transition (Id "'TrafficConflictHandler") Executing Finishing],
                        Micro $ Set.fromList [Transition (Id "'TrafficConflictHandler") Finishing IterationEnded],
                        Micro $ Set.fromList [Transition (Id "'TrafficConflictHandler") IterationEnded Finished]
                      ],
                    Macro [],
                    Macro []
                  ]
              )