#! /usr/bin/env bash

#set -xe

filename="$1"

declare -A count
declare -A count_fail
declare -A sum_elapsed

total_count=0
total_count_fail=0

while IFS=, read -r time_stamp elapsed label success bytes responseCode ; do
  if [[ -z count[$label] ]]; then
    count[$label]=0
    count_fail[$label]=0
    sum_elapsed[$label]=0
  fi

  ((total_count+=1))
  ((count["$label"]+=1))
  if [[ $success == 'false' ]]; then
    ((total_count_fail+=1))
    ((count_fail["$label"]+=1))
  fi
  ((sum_elapsed["$label"]+=elapsed))
done < <(tail -n +2 "$filename")

status="pass"
total_failure_rate=$(( total_count_fail * 100 / total_count ))
if [[ $total_failure_rate -gt 5 ]]; then
  status="FAIL"
fi

echo "$status (errors: $total_failure_rate%) $filename"

for label in "${!count[@]}"; do
  # Report actions with failures or if their name starts with "[section]"
  if [[ ${count_fail["$label"]} -gt 0 || "$label" =~ ^\[section\] ]]; then
    failure_rate=$(( count_fail["$label"] * 100 / count["$label"] ))
    status='ok'
    if [[ ${count_fail["$label"]} -gt 0 ]]; then
      status="$failure_rate%"
    fi
    avg_dur=$(( sum_elapsed[$label] / count["$label"] ))
    printf "     %-8s %-60s Avg: %s\n" "$status" "$label" "$avg_dur"
  fi
done | sort
echo
