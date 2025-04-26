open Lib

let () =
  let a = read_int () in
  let b = read_int () in
  let result = add a b in
  Printf.printf "%d\n" result