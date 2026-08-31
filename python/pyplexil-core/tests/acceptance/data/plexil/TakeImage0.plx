<?xml version="1.0" encoding="UTF-8"?>
<PlexilPlan xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
             FileName="TakeImage0.ple">
   <GlobalDeclarations ColNo="8" LineNo="4">
      <StateDeclaration ColNo="8" LineNo="4">
         <Name>PointedAtTarget</Name>
         <Return>
            <Name>_return_0</Name>
            <Type>Boolean</Type>
         </Return>
      </StateDeclaration>
      <CommandDeclaration ColNo="0" LineNo="6">
         <Name>camera_capture_image</Name>
         <Parameter>
            <Type>Integer</Type>
         </Parameter>
         <Parameter>
            <Type>Integer</Type>
         </Parameter>
      </CommandDeclaration>
      <CommandDeclaration ColNo="0" LineNo="7">
         <Name>slew</Name>
         <Parameter>
            <Type>Integer</Type>
         </Parameter>
         <Parameter>
            <Type>Real</Type>
         </Parameter>
         <Parameter>
            <Type>Real</Type>
         </Parameter>
      </CommandDeclaration>
   </GlobalDeclarations>
   <Node NodeType="NodeList" epx="CheckedSequence" ColNo="0" LineNo="9">
      <NodeId>TakeImage0</NodeId>
      <InvariantCondition>
         <NoChildFailed>
            <NodeRef dir="self"/>
         </NoChildFailed>
      </InvariantCondition>
      <NodeBody>
         <NodeList>
            <Node NodeType="NodeList" epx="Sequence" ColNo="2" LineNo="11">
               <NodeId>Slew</NodeId>
               <EndCondition ColNo="4" LineNo="13">
                  <LookupOnChange epx="Lookup">
                     <Name>
                        <StringValue>PointedAtTarget</StringValue>
                     </Name>
                  </LookupOnChange>
               </EndCondition>
               <InvariantCondition>
                  <NoChildFailed>
                     <NodeRef dir="self"/>
                  </NoChildFailed>
               </InvariantCondition>
               <NodeBody>
                  <NodeList>
                     <Node NodeType="Command"
                            epx="SynchronousCommand"
                            ColNo="4"
                            LineNo="15">
                        <NodeId>Slew1</NodeId>
                        <EndCondition>
                           <EQInternal>
                              <NodeCommandHandleVariable>
                                 <NodeRef dir="self"/>
                              </NodeCommandHandleVariable>
                              <NodeCommandHandleValue>COMMAND_SUCCESS</NodeCommandHandleValue>
                           </EQInternal>
                        </EndCondition>
                        <NodeBody>
                           <Command ColNo="30" LineNo="15">
                              <Name>
                                 <StringValue>slew</StringValue>
                              </Name>
                              <Arguments ColNo="35" LineNo="15">
                                 <IntegerValue>10</IntegerValue>
                                 <RealValue>-90.0</RealValue>
                                 <RealValue>0.0</RealValue>
                              </Arguments>
                           </Command>
                        </NodeBody>
                     </Node>
                  </NodeList>
               </NodeBody>
            </Node>
            <Node NodeType="NodeList" epx="Sequence" ColNo="2" LineNo="18">
               <NodeId>CaptureImage</NodeId>
               <StartCondition>
                  <Finished>
                     <NodeRef dir="sibling">Slew</NodeRef>
                  </Finished>
               </StartCondition>
               <PreCondition ColNo="4" LineNo="20">
                  <LookupNow epx="Lookup">
                     <Name>
                        <StringValue>PointedAtTarget</StringValue>
                     </Name>
                  </LookupNow>
               </PreCondition>
               <InvariantCondition>
                  <AND>
                     <LookupNow epx="Lookup">
                        <Name>
                           <StringValue>PointedAtTarget</StringValue>
                        </Name>
                     </LookupNow>
                     <NoChildFailed>
                        <NodeRef dir="self"/>
                     </NoChildFailed>
                  </AND>
               </InvariantCondition>
               <NodeBody>
                  <NodeList>
                     <Node NodeType="Command"
                            epx="SynchronousCommand"
                            ColNo="4"
                            LineNo="23">
                        <NodeId>CaptureImage1</NodeId>
                        <EndCondition>
                           <EQInternal>
                              <NodeCommandHandleVariable>
                                 <NodeRef dir="self"/>
                              </NodeCommandHandleVariable>
                              <NodeCommandHandleValue>COMMAND_SUCCESS</NodeCommandHandleValue>
                           </EQInternal>
                        </EndCondition>
                        <NodeBody>
                           <Command ColNo="38" LineNo="23">
                              <Name>
                                 <StringValue>camera_capture_image</StringValue>
                              </Name>
                              <Arguments ColNo="59" LineNo="23">
                                 <IntegerValue>50</IntegerValue>
                                 <IntegerValue>1</IntegerValue>
                              </Arguments>
                           </Command>
                        </NodeBody>
                     </Node>
                  </NodeList>
               </NodeBody>
            </Node>
         </NodeList>
      </NodeBody>
   </Node>
</PlexilPlan>
