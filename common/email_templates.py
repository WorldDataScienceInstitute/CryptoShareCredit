def send_funds_template(transaction_id, blockchain, network ,tx_amount, tx_currency, tx_address, creation_date):
    return """
    <!DOCTYPE html>

<html lang="en" xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:v="urn:schemas-microsoft-com:vml">

<head>
	<title></title>
	<meta content="text/html; charset=utf-8" http-equiv="Content-Type" />
	<meta content="width=device-width, initial-scale=1.0" name="viewport" />
	<!--[if mso]><xml><o:OfficeDocumentSettings><o:PixelsPerInch>96</o:PixelsPerInch><o:AllowPNG/></o:OfficeDocumentSettings></xml><![endif]-->
	<style>
		* \{
			box-sizing: border-box;
		\}

		body \{
			margin: 0;
			padding: 0;
		\}

		a[x-apple-data-detectors] {
			color: inherit !important;
			text-decoration: inherit !important;
		}

		#MessageViewBody a {
			color: inherit;
			text-decoration: none;
		}

		p {
			line-height: inherit
		}

		@media (max-width:660px) {
			.icons-inner {
				text-align: center;
			}

			.icons-inner td {
				margin: 0 auto;
			}

			.row-content {
				width: 100% !important;
			}

			.image_block img.big {
				width: auto !important;
			}

			.column .border {
				display: none;
			}

			table {
				table-layout: fixed !important;
			}

			.stack .column {
				width: 100%;
				display: block;
			}

			.row-5 .column-2 {
				border-right: 20px solid #FFF;
			}
		}
	</style>
</head>
""" + f"""
<body style="background-color: #f8f8f9; margin: 0; padding: 0; -webkit-text-size-adjust: none; text-size-adjust: none;">
	<table border="0" cellpadding="0" cellspacing="0" class="nl-container" role="presentation"
		style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #f8f8f9;" width="100%">
		<tbody>
			<tr>
				<td>
					<table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-1"
						role="presentation"
						style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #1aa19c;" width="100%">
						<tbody>
							<tr>
								<td>
									<table align="center" border="0" cellpadding="0" cellspacing="0"
										class="row-content stack" role="presentation"
										style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #1aa19c; color: #000000; width: 640px;"
										width="640">
										<tbody>
											<tr>
												<td class="column column-1"
													style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; vertical-align: top; padding-top: 0px; padding-bottom: 0px; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;"
													width="100%">
													<table border="0" cellpadding="0" cellspacing="0"
														class="divider_block" role="presentation"
														style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"
														width="100%">
														<tr>
															<td>
																<div align="center">
																	<table border="0" cellpadding="0" cellspacing="0"
																		role="presentation"
																		style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"
																		width="100%">
																		<tr>
																			<td class="divider_inner"
																				style="font-size: 1px; line-height: 1px; border-top: 4px solid #1AA19C;">
																				<span> </span></td>
																		</tr>
																	</table>
																</div>
															</td>
														</tr>
													</table>
												</td>
											</tr>
										</tbody>
									</table>
								</td>
							</tr>
						</tbody>
					</table>
					<table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-2"
						role="presentation"
						style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #fff;" width="100%">
						<tbody>
							<tr>
								<td>
									<table align="center" border="0" cellpadding="0" cellspacing="0"
										class="row-content stack" role="presentation"
										style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #fff; color: #000000; width: 640px;"
										width="640">
										<tbody>
											<tr>
												<td class="column column-1"
													style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; vertical-align: top; padding-top: 0px; padding-bottom: 0px; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;"
													width="100%">
													<table border="0" cellpadding="0" cellspacing="0"
														class="image_block" role="presentation"
														style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"
														width="100%">
														<tr>
															<td
																style="padding-bottom:25px;padding-top:22px;width:100%;padding-right:0px;padding-left:0px;">
																<div align="center" style="line-height:10px"><img
																		alt="I'm an image" class="big"
																		src="https://www.cryptoshareapp.com/static/images/CSlogo.png"
																		style="display: block; height: auto; border: 0; width: 640px; max-width: 100%;"
																		title="I'm an image" width="640" /></div>
															</td>
														</tr>
													</table>
												</td>
											</tr>
										</tbody>
									</table>
								</td>
							</tr>
						</tbody>
					</table>
					<table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-3"
						role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
						<tbody>
							<tr>
								<td>
									<table align="center" border="0" cellpadding="0" cellspacing="0"
										class="row-content stack" role="presentation"
										style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #f8f8f9; color: #000000; width: 640px;"
										width="640">
										<tbody>
											<tr>
												<td class="column column-1"
													style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; vertical-align: top; padding-top: 5px; padding-bottom: 5px; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;"
													width="100%">
													<table border="0" cellpadding="20" cellspacing="0"
														class="divider_block" role="presentation"
														style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"
														width="100%">
														<tr>
															<td>
																<div align="center">
																	<table border="0" cellpadding="0" cellspacing="0"
																		role="presentation"
																		style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"
																		width="100%">
																		<tr>
																			<td class="divider_inner"
																				style="font-size: 1px; line-height: 1px; border-top: 0px solid #BBBBBB;">
																				<span> </span></td>
																		</tr>
																	</table>
																</div>
															</td>
														</tr>
													</table>
												</td>
											</tr>
										</tbody>
									</table>
								</td>
							</tr>
						</tbody>
					</table>
					<table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-4"
						role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
						<tbody>
							<tr>
								<td>
									<table align="center" border="0" cellpadding="0" cellspacing="0"
										class="row-content stack" role="presentation"
										style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #fff; color: #000000; width: 640px;"
										width="640">
										<tbody>
											<tr>
												<td class="column column-1"
													style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; vertical-align: top; padding-top: 0px; padding-bottom: 0px; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;"
													width="100%">
													<table border="0" cellpadding="0" cellspacing="0"
														class="divider_block" role="presentation"
														style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"
														width="100%">
														<tr>
															<td style="padding-bottom:12px;padding-top:60px;">
																<div align="center">
																	<table border="0" cellpadding="0" cellspacing="0"
																		role="presentation"
																		style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"
																		width="100%">
																		<tr>
																			<td class="divider_inner"
																				style="font-size: 1px; line-height: 1px; border-top: 0px solid #BBBBBB;">
																				<span> </span></td>
																		</tr>
																	</table>
																</div>
															</td>
														</tr>
													</table>
													<table border="0" cellpadding="0" cellspacing="0"
														class="image_block" role="presentation"
														style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"
														width="100%">
														<tr>
															<td
																style="padding-left:40px;padding-right:40px;width:100%;">
																<div align="center" style="line-height:10px"><img
																		alt="I'm an image" src="https://www.cryptoshareapp.com/static/images/email_money.jpg"
																		style="display: block; height: auto; border: 0; width: 352px; max-width: 100%;"
																		title="I'm an image" width="352" /></div>
															</td>
														</tr>
													</table>
													<table border="0" cellpadding="0" cellspacing="0"
														class="divider_block" role="presentation"
														style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"
														width="100%">
														<tr>
															<td style="padding-top:50px;">
																<div align="center">
																	<table border="0" cellpadding="0" cellspacing="0"
																		role="presentation"
																		style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"
																		width="100%">
																		<tr>
																			<td class="divider_inner"
																				style="font-size: 1px; line-height: 1px; border-top: 0px solid #BBBBBB;">
																				<span> </span></td>
																		</tr>
																	</table>
																</div>
															</td>
														</tr>
													</table>
													<table border="0" cellpadding="0" cellspacing="0" class="text_block"
														role="presentation"
														style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;"
														width="100%">
														<tr>
															<td
																style="padding-bottom:10px;padding-left:40px;padding-right:40px;padding-top:10px;">
																<div style="font-family: sans-serif">
																	<div class="txtTinyMce-wrapper"
																		style="font-size: 12px; mso-line-height-alt: 14.399999999999999px; color: #555555; line-height: 1.2; font-family: Montserrat, Trebuchet MS, Lucida Grande, Lucida Sans Unicode, Lucida Sans, Tahoma, sans-serif;">
																		<p
																			style="margin: 0; font-size: 16px; text-align: center;">
																			<span
																				style="font-size:30px;color:#2b303a;"><strong>You
																					have just received
																					money!</strong></span></p>
																	</div>
																</div>
															</td>
														</tr>
													</table>
													<table border="0" cellpadding="0" cellspacing="0" class="text_block"
														role="presentation"
														style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;"
														width="100%">
														<tr>
															<td
																style="padding-bottom:10px;padding-left:40px;padding-right:40px;padding-top:10px;">
																<div style="font-family: sans-serif">
																	<div class="txtTinyMce-wrapper"
																		style="font-size: 12px; font-family: Montserrat, Trebuchet MS, Lucida Grande, Lucida Sans Unicode, Lucida Sans, Tahoma, sans-serif; mso-line-height-alt: 18px; color: #555555; line-height: 1.5;">
																		<p
																			style="margin: 0; font-size: 14px; text-align: center; mso-line-height-alt: 22.5px;">
																			<span
																				style="color:#808389;font-size:15px;">
																				Hi! You have just received a deposit into your Crypto$hare Account.	
																			</span></p>
																		<p
																			style="margin: 0; font-size: 14px; text-align: center; mso-line-height-alt: 22.5px;">
																			<span
																				style="color:#808389;font-size:15px;">
																				More details:
																		</span></p>
																	</div>
																</div>
															</td>
														</tr>
													</table>
													<table border="0" cellpadding="0" cellspacing="0"
														class="divider_block" role="presentation"
														style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"
														width="100%">
														<tr>
															<td style="padding-top:50px;">
																<div align="center">
																	<table border="0" cellpadding="0" cellspacing="0"
																		role="presentation"
																		style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"
																		width="100%">
																		<tr>
																			<td class="divider_inner"
																				style="font-size: 1px; line-height: 1px; border-top: 0px solid #BBBBBB;">
																				<span> </span></td>
																		</tr>
																	</table>
																</div>
															</td>
														</tr>
													</table>
												</td>
											</tr>
										</tbody>
									</table>
								</td>
							</tr>
						</tbody>
					</table>
					<table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-5"
						role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
						<tbody>
							<tr>
								<td>
									<table align="center" border="0" cellpadding="0" cellspacing="0" class="row-content"
										role="presentation"
										style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #fff; color: #000000; width: 640px;"
										width="640">
										<tbody>
											<tr>
												<td class="column column-1"
													style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; vertical-align: top;"
													width="50%">
													<table border="0" cellpadding="0" cellspacing="0"
														role="presentation"
														style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"
														width="100%">
														<tr>
															<td class="border" style="width:10px; background-color:#FFF">
																 </td>
															<td class="content_blocks"
																style="background-color:#f3fafa;border-right:8px solid #FFF;border-top:0px;border-bottom:0px;width:300px;">
																<table border="0" cellpadding="0" cellspacing="0"
																	class="divider_block" role="presentation"
																	style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"
																	width="100%">
																	<tr>
																		<td>
																			<div align="center">
																				<table border="0" cellpadding="0"
																					cellspacing="0" role="presentation"
																					style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"
																					width="100%">
																					<tr>
																						<td class="divider_inner"
																							style="font-size: 1px; line-height: 1px; border-top: 4px solid #1AA19C;">
																							<span> </span></td>
																					</tr>
																				</table>
																			</div>
																		</td>
																	</tr>
																</table>
																<table border="0" cellpadding="0" cellspacing="0"
																	class="text_block" role="presentation"
																	style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;"
																	width="100%">
																	<tr>
																		<td
																			style="padding-bottom:40px;padding-left:5px;padding-right:5px;padding-top:35px;">
																			<div style="font-family: sans-serif">
																				<div class="txtTinyMce-wrapper"
																					style="font-size: 12px; mso-line-height-alt: 18px; color: #555555; line-height: 1.5; font-family: Montserrat, Trebuchet MS, Lucida Grande, Lucida Sans Unicode, Lucida Sans, Tahoma, sans-serif;">
																					<p
																						style="margin: 0; font-size: 16px; text-align: center; mso-line-height-alt: 18px;">
																						<span
																							style="color:#a2a9ad;font-size:12px;"><strong>
																								TRANSACTION ID
																								</strong></span>
																					</p>
																					<p
																						style="margin: 0; font-size: 16px; text-align: center; mso-line-height-alt: 30px;">
																						<span
																							style="color:#2b303a;font-size:20px;"><strong>{transaction_id}</strong></span>
																					</p>
																				</div>
																			</div>
																		</td>
																	</tr>
																</table>
															</td>
															<td class="border" style="width:5px; background-color:#FFF">
															 </td>
														</tr>
													</table>
												</td>
											</tr>
										</tbody>
									</table>
								</td>
							</tr>
							<tr>
								<td>
									<table align="center" border="0" cellpadding="0" cellspacing="0" class="row-content"
										role="presentation"
										style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #fff; color: #000000; width: 640px;"
										width="640">
										<tbody>
											<tr>
												<td class="column column-1"
													style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; vertical-align: top;"
													width="50%">
													<table border="0" cellpadding="0" cellspacing="0"
														role="presentation"
														style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"
														width="100%">
														<tr>
															<td class="border" style="width:20px;background-color:#FFF">
																 </td>
															<td class="content_blocks"
																style="background-color:#f3fafa;border-right:8px solid #FFF;border-top:0px;border-bottom:0px;width:300px;">
																<table border="0" cellpadding="0" cellspacing="0"
																	class="divider_block" role="presentation"
																	style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"
																	width="100%">
																	<tr>
																		<td>
																			<div align="center">
																				<table border="0" cellpadding="0"
																					cellspacing="0" role="presentation"
																					style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"
																					width="100%">
																					<tr>
																						<td class="divider_inner"
																							style="font-size: 1px; line-height: 1px; border-top: 4px solid #1AA19C;">
																							<span> </span></td>
																					</tr>
																				</table>
																			</div>
																		</td>
																	</tr>
																</table>
																<table border="0" cellpadding="0" cellspacing="0"
																	class="text_block" role="presentation"
																	style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;"
																	width="100%">
																	<tr>
																		<td
																			style="padding-bottom:40px;padding-left:5px;padding-right:5px;padding-top:35px;">
																			<div style="font-family: sans-serif">
																				<div class="txtTinyMce-wrapper"
																					style="font-size: 12px; mso-line-height-alt: 18px; color: #555555; line-height: 1.5; font-family: Montserrat, Trebuchet MS, Lucida Grande, Lucida Sans Unicode, Lucida Sans, Tahoma, sans-serif;">
																					<p
																						style="margin: 0; font-size: 16px; text-align: center; mso-line-height-alt: 18px;">
																						<span
																							style="color:#a2a9ad;font-size:12px;"><strong>
																								Transaction Creation Date
																								</strong></span>
																					</p>
																					<p
																						style="margin: 0; font-size: 16px; text-align: center; mso-line-height-alt: 30px;">
																						<span
																							style="color:#2b303a;font-size:20px;"><strong>{creation_date.strftime('%Y-%m-%d')}</strong></span>
																					</p>
																				</div>
																			</div>
																		</td>
																	</tr>
																</table>
															</td>
														</tr>
													</table>
												</td>
												<td class="column column-2"
													style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; vertical-align: top;"
													width="50%">
													<table border="0" cellpadding="0" cellspacing="0"
														role="presentation"
														style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"
														width="100%">
														<tr>
															<td class="content_blocks"
																style="background-color:#f3fafa;border-left:8px solid #FFF;border-top:0px;border-bottom:0px;width:300px;">
																<table border="0" cellpadding="0" cellspacing="0"
																	class="divider_block" role="presentation"
																	style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"
																	width="100%">
																	<tr>
																		<td>
																			<div align="center">
																				<table border="0" cellpadding="0"
																					cellspacing="0" role="presentation"
																					style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"
																					width="100%">
																					<tr>
																						<td class="divider_inner"
																							style="font-size: 1px; line-height: 1px; border-top: 4px solid #1AA19C;">
																							<span> </span></td>
																					</tr>
																				</table>
																			</div>
																		</td>
																	</tr>
																</table>
																<table border="0" cellpadding="0" cellspacing="0"
																	class="text_block" role="presentation"
																	style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;"
																	width="100%">
																	<tr>
																		<td
																			style="padding-bottom:40px;padding-left:5px;padding-right:5px;padding-top:35px;">
																			<div style="font-family: sans-serif">
																				<div class="txtTinyMce-wrapper"
																					style="font-size: 12px; mso-line-height-alt: 18px; color: #555555; line-height: 1.5; font-family: Montserrat, Trebuchet MS, Lucida Grande, Lucida Sans Unicode, Lucida Sans, Tahoma, sans-serif;">
																					<p
																						style="margin: 0; font-size: 16px; text-align: center; mso-line-height-alt: 18px;">
																						<span
																							style="color:#a2a9ad;font-size:12px;"><strong>Transaction Hour</strong></span>
																					</p>
																					<p
																						style="margin: 0; font-size: 16px; text-align: center; mso-line-height-alt: 30px;">
																						<span
																							style="color:#2b303a;font-size:20px;"><strong>{creation_date.strftime('%H:%M:%S')}</strong></span>
																					</p>
																				</div>
																			</div>
																		</td>
																	</tr>
																</table>
															</td>
															<td class="border" style="width:20px;background-color:#FFF">
																 </td>
														</tr>
													</table>
												</td>
											</tr>
										</tbody>
									</table>
								</td>
							</tr>
							<tr>
								<td>
									<table align="center" border="0" cellpadding="0" cellspacing="0" class="row-content"
										role="presentation"
										style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #fff; color: #000000; width: 640px;"
										width="640">
										<tbody>
											<tr>
												<td class="column column-1"
													style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; vertical-align: top;"
													width="50%">
													<table border="0" cellpadding="0" cellspacing="0"
														role="presentation"
														style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"
														width="100%">
														<tr>
															<td class="border" style="width:20px;background-color:#FFF">
																 </td>
															<td class="content_blocks"
																style="background-color:#f3fafa;border-right:8px solid #FFF;border-top:0px;border-bottom:0px;width:300px;">
																<table border="0" cellpadding="0" cellspacing="0"
																	class="divider_block" role="presentation"
																	style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"
																	width="100%">
																	<tr>
																		<td>
																			<div align="center">
																				<table border="0" cellpadding="0"
																					cellspacing="0" role="presentation"
																					style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"
																					width="100%">
																					<tr>
																						<td class="divider_inner"
																							style="font-size: 1px; line-height: 1px; border-top: 4px solid #1AA19C;">
																							<span> </span></td>
																					</tr>
																				</table>
																			</div>
																		</td>
																	</tr>
																</table>
																<table border="0" cellpadding="0" cellspacing="0"
																	class="text_block" role="presentation"
																	style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;"
																	width="100%">
																	<tr>
																		<td
																			style="padding-bottom:40px;padding-left:5px;padding-right:5px;padding-top:35px;">
																			<div style="font-family: sans-serif">
																				<div class="txtTinyMce-wrapper"
																					style="font-size: 12px; mso-line-height-alt: 18px; color: #555555; line-height: 1.5; font-family: Montserrat, Trebuchet MS, Lucida Grande, Lucida Sans Unicode, Lucida Sans, Tahoma, sans-serif;">
																					<p
																						style="margin: 0; font-size: 16px; text-align: center; mso-line-height-alt: 18px;">
																						<span
																							style="color:#a2a9ad;font-size:12px;"><strong>
																								Symbol
																								</strong></span>
																					</p>
																					<p
																						style="margin: 0; font-size: 16px; text-align: center; mso-line-height-alt: 30px;">
																						<span
																							style="color:#2b303a;font-size:20px;"><strong>{tx_currency['symbol']}</strong></span>
																					</p>
																				</div>
																			</div>
																		</td>
																	</tr>
																</table>
															</td>
														</tr>
													</table>
												</td>
												<td class="column column-2"
													style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; vertical-align: top;"
													width="50%">
													<table border="0" cellpadding="0" cellspacing="0"
														role="presentation"
														style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"
														width="100%">
														<tr>
															<td class="content_blocks"
																style="background-color:#f3fafa;border-left:8px solid #FFF;border-top:0px;border-bottom:0px;width:300px;">
																<table border="0" cellpadding="0" cellspacing="0"
																	class="divider_block" role="presentation"
																	style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"
																	width="100%">
																	<tr>
																		<td>
																			<div align="center">
																				<table border="0" cellpadding="0"
																					cellspacing="0" role="presentation"
																					style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"
																					width="100%">
																					<tr>
																						<td class="divider_inner"
																							style="font-size: 1px; line-height: 1px; border-top: 4px solid #1AA19C;">
																							<span> </span></td>
																					</tr>
																				</table>
																			</div>
																		</td>
																	</tr>
																</table>
																<table border="0" cellpadding="0" cellspacing="0"
																	class="text_block" role="presentation"
																	style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;"
																	width="100%">
																	<tr>
																		<td
																			style="padding-bottom:40px;padding-left:5px;padding-right:5px;padding-top:35px;">
																			<div style="font-family: sans-serif">
																				<div class="txtTinyMce-wrapper"
																					style="font-size: 12px; mso-line-height-alt: 18px; color: #555555; line-height: 1.5; font-family: Montserrat, Trebuchet MS, Lucida Grande, Lucida Sans Unicode, Lucida Sans, Tahoma, sans-serif;">
																					<p
																						style="margin: 0; font-size: 16px; text-align: center; mso-line-height-alt: 18px;">
																						<span
																							style="color:#a2a9ad;font-size:12px;"><strong>Currency</strong></span>
																					</p>
																					<p
																						style="margin: 0; font-size: 16px; text-align: center; mso-line-height-alt: 30px;">
																						<span
																							style="color:#2b303a;font-size:20px;"><strong>{tx_currency['currency_name']}</strong></span>
																					</p>
																				</div>
																			</div>
																		</td>
																	</tr>
																</table>
															</td>
															<td class="border" style="width:20px;background-color:#FFF">
																 </td>
														</tr>
													</table>
												</td>
											</tr>
										</tbody>
									</table>
								</td>
							</tr>
							<tr>
								<td>
									<table align="center" border="0" cellpadding="0" cellspacing="0" class="row-content"
										role="presentation"
										style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #fff; color: #000000; width: 640px;"
										width="640">
										<tbody>
											<tr>
												<td class="column column-1"
													style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; vertical-align: top;"
													width="50%">
													<table border="0" cellpadding="0" cellspacing="0"
														role="presentation"
														style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"
														width="100%">
														<tr>
															<td class="border" style="width:20px;background-color:#FFF">
																 </td>
															<td class="content_blocks"
																style="background-color:#f3fafa;border-right:8px solid #FFF;border-top:0px;border-bottom:0px;width:300px;">
																<table border="0" cellpadding="0" cellspacing="0"
																	class="divider_block" role="presentation"
																	style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"
																	width="100%">
																	<tr>
																		<td>
																			<div align="center">
																				<table border="0" cellpadding="0"
																					cellspacing="0" role="presentation"
																					style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"
																					width="100%">
																					<tr>
																						<td class="divider_inner"
																							style="font-size: 1px; line-height: 1px; border-top: 4px solid #1AA19C;">
																							<span> </span></td>
																					</tr>
																				</table>
																			</div>
																		</td>
																	</tr>
																</table>
																<table border="0" cellpadding="0" cellspacing="0"
																	class="text_block" role="presentation"
																	style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;"
																	width="100%">
																	<tr>
																		<td
																			style="padding-bottom:40px;padding-left:5px;padding-right:5px;padding-top:35px;">
																			<div style="font-family: sans-serif">
																				<div class="txtTinyMce-wrapper"
																					style="font-size: 12px; mso-line-height-alt: 18px; color: #555555; line-height: 1.5; font-family: Montserrat, Trebuchet MS, Lucida Grande, Lucida Sans Unicode, Lucida Sans, Tahoma, sans-serif;">
																					<p
																						style="margin: 0; font-size: 16px; text-align: center; mso-line-height-alt: 18px;">
																						<span
																							style="color:#a2a9ad;font-size:12px;"><strong>
																								Blockchain
																								</strong></span>
																					</p>
                                                                    """ + f"""
																					<p
																						style="margin: 0; font-size: 16px; text-align: center; mso-line-height-alt: 30px;">
																						<span
																							style="color:#2b303a;font-size:20px;"><strong>{blockchain}</strong></span>
																					</p>
																				</div>
																			</div>
																		</td>
																	</tr>
																</table>
															</td>
														</tr>
													</table>
												</td>
												<td class="column column-2"
													style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; vertical-align: top;"
													width="50%">
													<table border="0" cellpadding="0" cellspacing="0"
														role="presentation"
														style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"
														width="100%">
														<tr>
															<td class="content_blocks"
																style="background-color:#f3fafa;border-left:8px solid #FFF;border-top:0px;border-bottom:0px;width:300px;">
																<table border="0" cellpadding="0" cellspacing="0"
																	class="divider_block" role="presentation"
																	style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"
																	width="100%">
																	<tr>
																		<td>
																			<div align="center">
																				<table border="0" cellpadding="0"
																					cellspacing="0" role="presentation"
																					style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"
																					width="100%">
																					<tr>
																						<td class="divider_inner"
																							style="font-size: 1px; line-height: 1px; border-top: 4px solid #1AA19C;">
																							<span> </span></td>
																					</tr>
																				</table>
																			</div>
																		</td>
																	</tr>
																</table>
																<table border="0" cellpadding="0" cellspacing="0"
																	class="text_block" role="presentation"
																	style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;"
																	width="100%">
																	<tr>
																		<td
																			style="padding-bottom:40px;padding-left:5px;padding-right:5px;padding-top:35px;">
																			<div style="font-family: sans-serif">
																				<div class="txtTinyMce-wrapper"
																					style="font-size: 12px; mso-line-height-alt: 18px; color: #555555; line-height: 1.5; font-family: Montserrat, Trebuchet MS, Lucida Grande, Lucida Sans Unicode, Lucida Sans, Tahoma, sans-serif;">
																					<p
																						style="margin: 0; font-size: 16px; text-align: center; mso-line-height-alt: 18px;">
																						<span
																							style="color:#a2a9ad;font-size:12px;"><strong>Network</strong></span>
																					</p>
																					<p
																						style="margin: 0; font-size: 16px; text-align: center; mso-line-height-alt: 30px;">
																						<span
																							style="color:#2b303a;font-size:20px;"><strong>{network}</strong></span>
																					</p>
																				</div>
																			</div>
																		</td>
																	</tr>
																</table>
															</td>
															<td class="border" style="width:20px;background-color:#FFF">
																 </td>
														</tr>
													</table>
												</td>
											</tr>
										</tbody>
									</table>
								</td>
							</tr>
							<tr>
								<td>
									<table align="center" border="0" cellpadding="0" cellspacing="0" class="row-content"
										role="presentation"
										style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #fff; color: #000000; width: 640px;"
										width="640">
										<tbody>
											<tr>
												<td class="column column-1"
													style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; vertical-align: top;"
													width="50%">
													<table border="0" cellpadding="0" cellspacing="0"
														role="presentation"
														style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"
														width="100%">
														<tr>
															<td class="border" style="width:10px; background-color:#FFF">
																 </td>
															<td class="content_blocks"
																style="background-color:#f3fafa;border-right:8px solid #FFF;border-top:0px;border-bottom:0px;width:300px;">
																<table border="0" cellpadding="0" cellspacing="0"
																	class="divider_block" role="presentation"
																	style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"
																	width="100%">
																	<tr>
																		<td>
																			<div align="center">
																				<table border="0" cellpadding="0"
																					cellspacing="0" role="presentation"
																					style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"
																					width="100%">
																					<tr>
																						<td class="divider_inner"
																							style="font-size: 1px; line-height: 1px; border-top: 4px solid #1AA19C;">
																							<span> </span></td>
																					</tr>
																				</table>
																			</div>
																		</td>
																	</tr>
																</table>
																<table border="0" cellpadding="0" cellspacing="0"
																	class="text_block" role="presentation"
																	style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;"
																	width="100%">
																	<tr>
																		<td
																			style="padding-bottom:40px;padding-left:5px;padding-right:5px;padding-top:35px;">
																			<div style="font-family: sans-serif">
																				<div class="txtTinyMce-wrapper"
																					style="font-size: 12px; mso-line-height-alt: 18px; color: #555555; line-height: 1.5; font-family: Montserrat, Trebuchet MS, Lucida Grande, Lucida Sans Unicode, Lucida Sans, Tahoma, sans-serif;">
																					<p
																						style="margin: 0; font-size: 16px; text-align: center; mso-line-height-alt: 18px;">
																						<span
																							style="color:#a2a9ad;font-size:12px;"><strong>
																								Amount
																								</strong></span>
																					</p>
																					<p
																						style="margin: 0; font-size: 16px; text-align: center; mso-line-height-alt: 30px;">
																						<span
																							style="color:#2b303a;font-size:20px;"><strong>{tx_amount}</strong></span>
																					</p>
																				</div>
																			</div>
																		</td>
																	</tr>
																</table>
															</td>
															<td class="border" style="width:5px; background-color:#FFF">
															 </td>
														</tr>
													</table>
												</td>
											</tr>
										</tbody>
									</table>
								</td>
							</tr>
						</tbody>
					</table>
					<table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-6"
						role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
						<tbody>
							<tr>
								<td>
									<table align="center" border="0" cellpadding="0" cellspacing="0"
										class="row-content stack" role="presentation"
										style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #fff; color: #000000; width: 640px;"
										width="640">
										<tbody>
											<tr>
												<td class="column column-1"
													style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; vertical-align: top; padding-top: 0px; padding-bottom: 0px; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;"
													width="100%">
													<table border="0" cellpadding="0" cellspacing="0"
														class="divider_block" role="presentation"
														style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"
														width="100%">
														<tr>
															<td style="padding-bottom:12px;padding-top:60px;">
																<div align="center">
																	<table border="0" cellpadding="0" cellspacing="0"
																		role="presentation"
																		style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"
																		width="100%">
																		<tr>
																			<td class="divider_inner"
																				style="font-size: 1px; line-height: 1px; border-top: 0px solid #BBBBBB;">
																				<span> </span></td>
																		</tr>
																	</table>
																</div>
															</td>
														</tr>
													</table>
												</td>
											</tr>
										</tbody>
									</table>
								</td>
							</tr>
							<tr>
								<td>
									<table align="center" border="0" cellpadding="0" cellspacing="0" class="row-content"
										role="presentation"
										style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #fff; color: #000000; width: 640px;"
										width="640">
										<tbody>
											<tr>
												<td class="column column-1"
													style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; vertical-align: top;"
													width="50%">
													<table border="0" cellpadding="0" cellspacing="0"
														role="presentation"
														style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"
														width="100%">
														<tr>
															<td class="border" style="width:10px; background-color:#FFF">
																 </td>
															<td class="content_blocks"
																style="background-color:#f3fafa;border-right:8px solid #FFF;border-top:0px;border-bottom:0px;width:300px;">
																<table border="0" cellpadding="0" cellspacing="0"
																	class="divider_block" role="presentation"
																	style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"
																	width="100%">
																	<tr>
																		<td>
																			<div align="center">
																				<table border="0" cellpadding="0"
																					cellspacing="0" role="presentation"
																					style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"
																					width="100%">
																					<tr>
																						<td class="divider_inner"
																							style="font-size: 1px; line-height: 1px; border-top: 4px solid #1AA19C;">
																							<span> </span></td>
																					</tr>
																				</table>
																			</div>
																		</td>
																	</tr>
																</table>
																<table border="0" cellpadding="0" cellspacing="0"
																	class="text_block" role="presentation"
																	style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;"
																	width="100%">
																	<tr>
																		<td
																			style="padding-bottom:40px;padding-left:5px;padding-right:5px;padding-top:35px;">
																			<div style="font-family: sans-serif">
																				<div class="txtTinyMce-wrapper"
																					style="font-size: 12px; mso-line-height-alt: 18px; color: #555555; line-height: 1.5; font-family: Montserrat, Trebuchet MS, Lucida Grande, Lucida Sans Unicode, Lucida Sans, Tahoma, sans-serif;">
																					<p
																						style="margin: 0; font-size: 16px; text-align: center; mso-line-height-alt: 18px;">
																						<span
																							style="color:#a2a9ad;font-size:12px;"><strong>
																								Customer Support Transaction ID:
																								</strong></span>
																					</p>
																					<p
																						style="margin: 0; font-size: 16px; text-align: center; mso-line-height-alt: 30px;">
																						<span
																							style="color:#2b303a;font-size:20px;"><strong>{transaction_id}</strong></span>
																					</p>
																				</div>
																			</div>
																		</td>
																	</tr>
																</table>
															</td>
															<td class="border" style="width:5px; background-color:#FFF">
															 </td>
														</tr>
													</table>
												</td>
											</tr>
										</tbody>
									</table>
								</td>
							</tr>
						</tbody>
					</table>
					<table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-7"
						role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
						<tbody>
							<tr>
								<td>
									<table align="center" border="0" cellpadding="0" cellspacing="0"
										class="row-content stack" role="presentation"
										style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #f8f8f9; color: #000000; width: 640px;"
										width="640">
										<tbody>
											<tr>
												<td class="column column-1"
													style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; vertical-align: top; padding-top: 5px; padding-bottom: 5px; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;"
													width="100%">
													<table border="0" cellpadding="20" cellspacing="0"
														class="divider_block" role="presentation"
														style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"
														width="100%">
														<tr>
															<td>
																<div align="center">
																	<table border="0" cellpadding="0" cellspacing="0"
																		role="presentation"
																		style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"
																		width="100%">
																		<tr>
																			<td class="divider_inner"
																				style="font-size: 1px; line-height: 1px; border-top: 0px solid #BBBBBB;">
																				<span> </span></td>
																		</tr>
																	</table>
																</div>
															</td>
														</tr>
													</table>
												</td>
											</tr>
										</tbody>
									</table>
								</td>
							</tr>
						</tbody>
					</table>
					<table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-8"
						role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
						<tbody>
							<tr>
								<td>
									<table align="center" border="0" cellpadding="0" cellspacing="0"
										class="row-content stack" role="presentation"
										style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #2b303a; color: #000000; width: 640px;"
										width="640">
										<tbody>
											<tr>
												<td class="column column-1"
													style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; vertical-align: top; padding-top: 0px; padding-bottom: 0px; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;"
													width="100%">
													<table border="0" cellpadding="0" cellspacing="0"
														class="divider_block" role="presentation"
														style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"
														width="100%">
														<tr>
															<td>
																<div align="center">
																	<table border="0" cellpadding="0" cellspacing="0"
																		role="presentation"
																		style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"
																		width="100%">
																		<tr>
																			<td class="divider_inner"
																				style="font-size: 1px; line-height: 1px; border-top: 4px solid #1AA19C;">
																				<span> </span></td>
																		</tr>
																	</table>
																</div>
															</td>
														</tr>
													</table>
													<table border="0" cellpadding="0" cellspacing="0"
														class="image_block" role="presentation"
														style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"
														width="100%">
														<tr>
															<td style="width:100%;padding-right:0px;padding-left:0px;">
																<div align="center" style="line-height:10px"><img
																		alt="I'm an image" class="big"
																		src="https://www.cryptoshareapp.com/static/images/email_footer.png"
																		style="display: block; height: auto; border: 0; width: 640px; max-width: 100%;"
																		title="I'm an image" width="640" /></div>
															</td>
														</tr>
													</table>
													<table border="0" cellpadding="0" cellspacing="0"
														class="image_block" role="presentation"
														style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"
														width="100%">
														<tr>
															<td
																style="padding-top:40px;width:100%;padding-right:0px;padding-left:0px;">
																<div align="center" style="line-height:10px"><img
																		alt="Alternate text" src="https://www.cryptoshareapp.com/static/images/CSlogo.png"
																		style="display: block; height: auto; border: 0; width: 192px; max-width: 100%;"
																		title="Alternate text" width="192" /></div>
															</td>
														</tr>
													</table>
													<table border="0" cellpadding="0" cellspacing="0" class="text_block"
														role="presentation"
														style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;"
														width="100%">
														<tr>
															<td
																style="padding-bottom:10px;padding-left:40px;padding-right:40px;padding-top:15px;">
																<div style="font-family: sans-serif">
																	<div class="txtTinyMce-wrapper"
																		style="font-size: 12px; font-family: Montserrat, Trebuchet MS, Lucida Grande, Lucida Sans Unicode, Lucida Sans, Tahoma, sans-serif; mso-line-height-alt: 18px; color: #555555; line-height: 1.5;">
																		<p
																			style="margin: 0; font-size: 14px; text-align: left; mso-line-height-alt: 18px;">
																			<span
																				style="color:#95979c;font-size:12px;">If this was not you, please secure your account at <a href="http://www.cryptoshareapp.com/">Crypto$hare</a>.</span>
																		</p>
																	</div>
																</div>
															</td>
														</tr>
													</table>
													<table border="0" cellpadding="0" cellspacing="0"
														class="divider_block" role="presentation"
														style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"
														width="100%">
														<tr>
															<td
																style="padding-bottom:10px;padding-left:40px;padding-right:40px;padding-top:25px;">
																<div align="center">
																	<table border="0" cellpadding="0" cellspacing="0"
																		role="presentation"
																		style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"
																		width="100%">
																		<tr>
																			<td class="divider_inner"
																				style="font-size: 1px; line-height: 1px; border-top: 1px solid #555961;">
																				<span> </span></td>
																		</tr>
																	</table>
																</div>
															</td>
														</tr>
													</table>
													<table border="0" cellpadding="0" cellspacing="0" class="text_block"
														role="presentation"
														style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;"
														width="100%">
														<tr>
															<td
																style="padding-bottom:30px;padding-left:40px;padding-right:40px;padding-top:20px;">
																<div style="font-family: sans-serif">
																	<div class="txtTinyMce-wrapper"
																		style="font-size: 12px; font-family: Montserrat, Trebuchet MS, Lucida Grande, Lucida Sans Unicode, Lucida Sans, Tahoma, sans-serif; mso-line-height-alt: 14.399999999999999px; color: #555555; line-height: 1.2;">
																		<p
																			style="margin: 0; font-size: 14px; text-align: left;">
																			<span
																				style="color:#95979c;font-size:12px;">Crypto$hare
																				Copyright © 2022</span></p>
																	</div>
																</div>
															</td>
														</tr>
													</table>
												</td>
											</tr>
										</tbody>
									</table>
								</td>
							</tr>
						</tbody>
					</table>
				</td>
			</tr>
		</tbody>
	</table><!-- End -->
</body>

</html>
"""