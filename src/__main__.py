import socket
import os
import sys
import time
import argparse
import config


def action_send(args):
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
		server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		
		server_socket.bind((args.host, args.port))
		server_socket.listen(1)
		
		client_socket, client_address = server_socket.accept()
		with client_socket:
			with open(args.input_path, "rb") as f:
				while True:
					b = f.read(args.chunk_size)
					
					if len(b) == 0:
						break
					
					client_socket.sendall(b)


def action_recv(args):
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
		server_socket.connect((args.host, args.port))
		
		with open(args.output_path, "wb") as f:
			while True:
				b = server_socket.recv(args.chunk_size)
				
				if len(b) == 0:
					break
				
				f.write(b)


def parse_args():
	parser = argparse.ArgumentParser()
	
	parser.add_argument("-v", "--version", action="version",
		version="%(name)s %(version)s" % {
			"name": config.program_name,
			"version": config.program_version,
		})
	
	subparsers = parser.add_subparsers(dest="action", required=True)
	
	parser_send = subparsers.add_parser("send")
	parser_send.set_defaults(action=action_send)
	
	parser_send.add_argument("input_path")
	
	parser_send.add_argument("--host", type=str,
		default=config.default_host)
	
	parser_send.add_argument("--port", type=int,
		default=config.default_port)
	
	parser_send.add_argument("--chunk-size", type=int,
		default=config.default_chunk_size)
	
	parser_recv = subparsers.add_parser("recv")
	parser_recv.set_defaults(action=action_recv)
	
	parser_recv.add_argument("output_path")
	
	parser_recv.add_argument("--host", type=str,
		default=config.default_host)
	
	parser_recv.add_argument("--port", type=int,
		default=config.default_port)
	
	parser_recv.add_argument("--chunk-size", type=int,
		default=config.default_chunk_size)
	
	return parser.parse_args()


def main():
	args = parse_args()
	args.action(args)


main()
