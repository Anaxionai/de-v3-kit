# TaxiScale plans

## Plan of the daily job

<!-- TODO(task 11): the output of explain("formatted"), in a code block. -->

## Shuffles

<!-- TODO(task 11): every Exchange node: its number, its partitioning and the line of code that causes it. Then each BroadcastExchange, and why it is not a shuffle. -->

## Stages

<!-- TODO(task 11): Shuffle Read and Shuffle Write of each stage, from the history server (http://localhost:18080). -->

| Stage | Shuffle Read | Shuffle Write |
|---|---|---|

## What I learned

<!-- TODO(task 11): the shuffle that moves the most data, and one idea to make it smaller. -->

## Baseline: sort-merge

<!-- TODO(task 12): the SortMergeJoin part of the plan, with an Exchange on each side. -->

## Broadcast

<!-- TODO(task 12): the BroadcastHashJoin part of the plan. -->

## Why

<!-- TODO(task 12): 3 to 5 sentences: which shuffles disappeared, and why the time changed or hardly changed. -->

## Skew

<!-- TODO(task 13): the hot zone, max against median before and after, what salting cost, and why AQE did not split the partition. -->
