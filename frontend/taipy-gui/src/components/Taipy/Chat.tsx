/*
 * Copyright 2021-2025 Avaiga Private Limited
 *
 * Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
 * the License. You may obtain a copy of the License at
 *
 *        http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
 * an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
 * specific language governing permissions and limitations under the License.
 */

import React, {
    useMemo,
    useCallback,
    KeyboardEvent,
    MouseEvent,
    useState,
    useRef,
    useEffect,
    ReactNode,
    lazy,
    ChangeEvent,
    UIEvent,
} from "react";
import { SxProps, Theme, darken, lighten } from "@mui/material/styles";
import Avatar from "@mui/material/Avatar";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Chip from "@mui/material/Chip";
import Grid from "@mui/material/Grid2";
import IconButton from "@mui/material/IconButton";
import InputAdornment from "@mui/material/InputAdornment";
import Paper from "@mui/material/Paper";
import Popper from "@mui/material/Popper";
import TextField from "@mui/material/TextField";
import Tooltip from "@mui/material/Tooltip";
import Send from "@mui/icons-material/Send";
import AttachFile from "@mui/icons-material/AttachFile";
import ArrowDownward from "@mui/icons-material/ArrowDownward";
import ArrowUpward from "@mui/icons-material/ArrowUpward";

import {
    createNotificationAction,
    createRequestInfiniteTableUpdateAction,
    createSendActionNameAction,
} from "../../context/pyforgeReducers";
import { PyForgeActiveProps, disableColor, getSuffixedClassNames } from "./utils";
import { useClassNames, useDispatch, useDynamicProperty, useElementVisible, useModule } from "../../utils/hooks";
import { LoVElt, useLovListMemo } from "./lovUtils";
import { IconAvatar, avatarSx } from "../../utils/icon";
import { emptyArray, getInitials } from "../../utils";
import { RowType, TableValueType } from "./tableUtils";
import { Stack } from "@mui/material";
import { getComponentClassName } from "./PyForgeStyle";
import { noDisplayStyle } from "./utils";
import { toDataUrl } from "../../utils/image";

const Markdown = lazy(() => import("react-markdown"));

interface ChatProps extends PyForgeActiveProps {
    messages?: TableValueType;
    maxFileSize?: number;
    withInput?: boolean;
    users?: LoVElt[];
    defaultUsers?: string;
    onAction?: string;
    senderId?: string;
    height?: string;
    defaultKey?: string; // for testing purposes only
    pageSize?: number;
    showSender?: boolean;
    mode?: string;
    allowSendImages?: boolean;
}

const ENTER_KEY = "Enter";

const indicWidth = 0.7;
const avatarWidth = 24;
const chatAvatarSx = { ...avatarSx, width: avatarWidth, height: avatarWidth };
const avatarColSx = { width: 1.5 * avatarWidth, minWidth: 1.5 * avatarWidth, pt: 1 };
const senderMsgSx = {
    width: "fit-content",
    maxWidth: "80%",
} as SxProps<Theme>;
const gridSx = { pb: "1em", mt: "unset", flex: 1, overflow: "auto" };
const loadMoreSx = { width: "fit-content", marginLeft: "auto", marginRight: "auto" };
const inputSx = { maxWidth: "unset" };
const leftNameSx = { fontSize: "0.6em", fontWeight: "bolder", pl: `${indicWidth}em` };
const rightNameSx: SxProps = {
    ...leftNameSx,
    pr: `${2 * indicWidth}em`,
    width: "100%",
    display: "flex",
    justifyContent: "flex-end",
};
const senderPaperSx = {
    pr: `${indicWidth}em`,
    pl: `${indicWidth}em`,
    mr: `${indicWidth}em`,
    position: "relative",
    "&:before": {
        content: "''",
        position: "absolute",
        width: "0",
        height: "0",
        borderTopWidth: `${indicWidth}em`,
        borderTopStyle: "solid",
        borderTopColor: (theme: Theme) => theme.palette.background.paper,
        borderLeft: `${indicWidth}em solid transparent`,
        borderRight: `${indicWidth}em solid transparent`,
        top: "0",
        right: `-${indicWidth}em`,
    },
} as SxProps<Theme>;
const otherPaperSx = {
    position: "relative",
    pl: `${indicWidth}em`,
    pr: `${indicWidth}em`,
    "&:before": {
        content: "''",
        position: "absolute",
        width: "0",
        height: "0",
        borderTopWidth: `${indicWidth}em`,
        borderTopStyle: "solid",
        borderTopColor: (theme: Theme) => theme.palette.background.paper,
        borderLeft: `${indicWidth}em solid transparent`,
        borderRight: `${indicWidth}em solid transparent`,
        top: "0",
        left: `-${indicWidth}em`,
    },
} as SxProps<Theme>;
const defaultBoxSx = {
    pl: `${indicWidth}em`,
    pr: `${indicWidth}em`,
    backgroundColor: (theme: Theme) =>
        theme.palette.mode == "dark"
            ? lighten(theme.palette.background.paper, 0.05)
            : darken(theme.palette.background.paper, 0.15),
} as SxProps<Theme>;
const noAnchorSx = { overflowAnchor: "none", "& *": { overflowAnchor: "none" } } as SxProps<Theme>;
const anchorSx = { overflowAnchor: "auto", height: "1px", width: "100%" } as SxProps<Theme>;
const imageSx = { width: 3 / 5, height: "auto" };
interface key2Rows {
    key: string;
}

interface ChatRowProps {
    senderId: string;
    message: string;
    image?: string;
    name: string;
    className?: string;
    getAvatar: (id: string, sender: boolean) => ReactNode;
    index: number;
    showSender: boolean;
    mode: string;
}

const ChatRow = (props: ChatRowProps) => {
    const { senderId, message, image, name, className, getAvatar, index, showSender, mode } = props;
    const sender = senderId == name;
    const avatar = getAvatar(name, sender);

    return (
        <Grid
            container
            className={getSuffixedClassNames(className, sender ? "-sent" : "-received")}
            size={12}
            sx={noAnchorSx}
            justifyContent={sender ? "flex-end" : undefined}
        >
            <Grid sx={sender ? senderMsgSx : undefined}>
                {image ? (
                    <Grid container justifyContent={sender ? "flex-end" : undefined}>
                        <Box component="img" sx={imageSx} alt="Uploaded image" src={image} />
                    </Grid>
                ) : null}
                {(!sender || showSender) && avatar ? (
                    <Stack direction="row" gap={1} justifyContent={sender ? "flex-end" : undefined}>
                        {!sender ? <Box sx={avatarColSx}>{avatar}</Box> : null}
                        <Stack>
                            <Box sx={sender ? rightNameSx : leftNameSx}>{name}</Box>
                            <Paper
                                sx={sender ? senderPaperSx : otherPaperSx}
                                data-idx={index}
                                className={getSuffixedClassNames(className, "-" + mode)}
                            >
                                {mode == "pre" ? (
                                    <pre>{message}</pre>
                                ) : mode == "raw" ? (
                                    message
                                ) : (
                                    <Markdown>{message}</Markdown>
                                )}
                            </Paper>
                        </Stack>
                        {sender ? <Box sx={avatarColSx}>{avatar}</Box> : null}
                    </Stack>
                ) : (
                    <Paper
                        sx={sender ? senderPaperSx : otherPaperSx}
                        data-idx={index}
                        className={getSuffixedClassNames(className, mode)}
                    >
                        {mode == "pre" ? (
                            <pre>{message}</pre>
                        ) : mode == "raw" ? (
                            message
                        ) : (
                            <Markdown>{message}</Markdown>
                        )}
                    </Paper>
                )}
            </Grid>
        </Grid>
    );
};

const getChatKey = (start: number, page: number) => `Chat-${start}-${start + page}`;

const Chat = (props: ChatProps) => {
    const {
        id,
        updateVarName,
        senderId = "pyforge",
        onAction,
        withInput = true,
        defaultKey = "",
        maxFileSize = .8 * 1024 * 1024, // 0.8 MB
        pageSize = 50,
        showSender = false,
        allowSendImages = true,
    } = props;
    const dispatch = useDispatch();
    const module = useModule();

    const [rows, setRows] = useState<RowType[]>([]);
    const page = useRef<key2Rows>({ key: defaultKey });
    const [columns, setColumns] = useState<Array<string>>([]);
    const scrollDivRef = useRef<HTMLDivElement>(null);
    const anchorDivRef = useRef<HTMLElement>(null);
    const isAnchorDivVisible = useElementVisible(anchorDivRef);
    const [enableSend, setEnableSend] = useState(false);
    const [showMessage, setShowMessage] = useState(false);
    const [anchorPopup, setAnchorPopup] = useState<HTMLDivElement | null>(null);
    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const [imagePreview, setImagePreview] = useState<string | null>(null);
    const [objectURLs, setObjectURLs] = useState<string[]>([]);
    const fileInputRef = useRef<HTMLInputElement>(null);
    const userScrolled = useRef(false);

    const className = useClassNames(props.libClassName, props.dynamicClassName, props.className);
    const active = useDynamicProperty(props.active, props.defaultActive, true);
    const hover = useDynamicProperty(props.hoverText, props.defaultHoverText, undefined);
    const users = useLovListMemo(props.users, props.defaultUsers || "");

    const mode = useMemo(
        () => (["pre", "raw"].includes(props.mode || "") ? (props.mode as string) : "markdown"),
        [props.mode]
    );
    const boxSx = useMemo(
        () =>
            props.height
                ? ({
                      ...defaultBoxSx,
                      maxHeight: "" + Number(props.height) == "" + props.height ? props.height + "px" : props.height,
                      display: "flex",
                      flexDirection: "column",
                  } as SxProps<Theme>)
                : defaultBoxSx,
        [props.height]
    );

    const onChangeHandler = useCallback((evt: ChangeEvent<HTMLInputElement>) => setEnableSend(!!evt.target.value), []);

    const sendAction = useCallback(
        (elt: HTMLInputElement | null | undefined, reason: string) => {
            if (elt && (elt?.value || imagePreview)) {
                toDataUrl(imagePreview)
                    .then((dataUrl) => {
                        dispatch(
                            createSendActionNameAction(
                                id,
                                module,
                                onAction,
                                reason,
                                updateVarName,
                                elt?.value,
                                senderId,
                                dataUrl
                            )
                        );
                        elt.value = "";
                        setSelectedFile(null);
                        setImagePreview((url) => {
                            url && URL.revokeObjectURL(url);
                            return null;
                        });
                        fileInputRef.current && (fileInputRef.current.value = "");
                    })
                    .catch(console.log);
            }
        },
        [imagePreview, updateVarName, onAction, senderId, id, dispatch, module]
    );

    const handleAction = useCallback(
        (evt: KeyboardEvent<HTMLDivElement>) => {
            if (!evt.shiftKey && !evt.ctrlKey && !evt.altKey && ENTER_KEY == evt.key) {
                sendAction(evt.currentTarget.querySelector("input"), evt.key);
                evt.preventDefault();
            }
        },
        [sendAction]
    );

    const handleClick = useCallback(
        (evt: MouseEvent<HTMLButtonElement>) => {
            sendAction(evt.currentTarget.parentElement?.parentElement?.querySelector("input"), "click");
            evt.preventDefault();
        },
        [sendAction]
    );

    const handleFileSelect = useCallback((event: React.ChangeEvent<HTMLInputElement>) => {
        const file = event.target.files ? event.target.files[0] : null;
        if (file) {
            if (file.type.startsWith("image/") && file.size <= maxFileSize) {
                setSelectedFile(file);
                const newImagePreview = URL.createObjectURL(file);
                setImagePreview(newImagePreview);
                setObjectURLs((prevURLs) => [...prevURLs, newImagePreview]);
            } else {
                dispatch(
                    createNotificationAction({
                        atype: "info",
                        message:
                            file.size > maxFileSize
                                ? `Image size is limited to ${maxFileSize / 1024} KB`
                                : "Only image file are authorized",
                        system: false,
                        duration: 3000,
                    })
                );
                setSelectedFile(null);
                setImagePreview(null);
                fileInputRef.current && (fileInputRef.current.value = "");
            }
        }
    }, [maxFileSize, dispatch]);

    const handleAttachClick = useCallback(() => fileInputRef.current && fileInputRef.current.click(), [fileInputRef]);

    const handleImageDelete = useCallback(() => {
        setSelectedFile(null);
        setImagePreview((url) => {
            url && URL.revokeObjectURL(url);
            return null;
        });
        fileInputRef.current && (fileInputRef.current.value = "");
    }, []);

    const avatars = useMemo(() => {
        return users.reduce((pv, elt) => {
            if (elt.id) {
                pv[elt.id] =
                    typeof elt.item == "string" ? (
                        <Tooltip title={elt.item}>
                            <Avatar sx={chatAvatarSx}>{getInitials(elt.item)}</Avatar>
                        </Tooltip>
                    ) : (
                        <IconAvatar img={elt.item} sx={chatAvatarSx} />
                    );
            }
            return pv;
        }, {} as Record<string, React.ReactNode>);
    }, [users]);

    const getAvatar = useCallback(
        (id: string, sender: boolean) =>
            avatars[id] ||
            (sender ? null : (
                <Tooltip title={id}>
                    <Avatar sx={chatAvatarSx}>{getInitials(id)}</Avatar>
                </Tooltip>
            )),
        [avatars]
    );

    const loadMoreItems = useCallback(
        (startIndex: number) => {
            const key = getChatKey(startIndex, pageSize);
            page.current = {
                key: key,
            };
            dispatch(
                createRequestInfiniteTableUpdateAction(
                    updateVarName,
                    id,
                    module,
                    [],
                    key,
                    startIndex,
                    startIndex + pageSize,
                    undefined,
                    undefined,
                    undefined,
                    undefined,
                    undefined,
                    undefined,
                    undefined,
                    undefined,
                    undefined,
                    undefined,
                    undefined,
                    undefined,
                    true // reverse
                )
            );
        },
        [pageSize, updateVarName, id, dispatch, module]
    );

    const showBottom = useCallback(() => {
        anchorDivRef.current?.scrollIntoView && anchorDivRef.current?.scrollIntoView();
        setShowMessage(false);
    }, []);

    const refresh = props.messages?.__pyforge_refresh !== undefined;

    useEffect(() => {
        if (!refresh && props.messages && page.current.key && props.messages[page.current.key] !== undefined) {
            const newValue = props.messages[page.current.key];
            if (newValue.rowcount == 0) {
                setRows(emptyArray);
            } else {
                const nr = newValue.data as RowType[];
                if (Array.isArray(nr) && nr.length > newValue.start && nr[newValue.start]) {
                    setRows((old) => {
                        old.length && nr.length > old.length && setShowMessage(true);
                        if (newValue.start > 0 && old.length > newValue.start) {
                            return old.slice(0, newValue.start).concat(nr.slice(newValue.start));
                        }
                        return nr;
                    });
                    const cols = Object.keys(nr[newValue.start]);
                    setColumns(cols.length > 2 ? cols : cols.length == 2 ? [...cols, ""] : ["", ...cols, "", ""]);
                }
            }
            page.current.key = getChatKey(0, pageSize);
            !userScrolled.current && showBottom();
        }
    }, [refresh, pageSize, props.messages, showBottom]);

    useEffect(() => {
        if (showMessage && !isAnchorDivVisible) {
            setAnchorPopup(scrollDivRef.current);
            setTimeout(() => setShowMessage(false), 5000);
        } else if (!showMessage) {
            setAnchorPopup(null);
        }
    }, [showMessage, isAnchorDivVisible]);

    useEffect(() => {
        if (refresh) {
            Promise.resolve().then(() => loadMoreItems(0)); // So that the state can be changed
        }
    }, [refresh, loadMoreItems]);

    useEffect(() => {
        loadMoreItems(0);
    }, [loadMoreItems]);

    useEffect(() => {
        return () => {
            for (const objectURL of objectURLs) {
                URL.revokeObjectURL(objectURL);
            }
        };
    }, [objectURLs]);

    const loadOlder = useCallback(
        (evt: MouseEvent<HTMLElement>) => {
            const { start } = evt.currentTarget.dataset;
            if (start) {
                loadMoreItems(parseInt(start));
            }
        },
        [loadMoreItems]
    );

    const handleOnScroll = useCallback((evt: UIEvent) => {
        userScrolled.current = (evt.target as HTMLDivElement).scrollHeight - (evt.target as HTMLDivElement).offsetHeight - (evt.target as HTMLDivElement).scrollTop > 1;
    }, []);

    return (
        <Tooltip title={hover || ""}>
            <Paper className={`${className} ${getComponentClassName(props.children)}`} sx={boxSx} id={id}>
                <Grid container rowSpacing={2} sx={gridSx} ref={scrollDivRef} onScroll={handleOnScroll}>
                    {rows.length && !rows[0] ? (
                        <Grid className={getSuffixedClassNames(className, "-load")} size={12} sx={noAnchorSx}>
                            <Box sx={loadMoreSx}>
                                <Button
                                    endIcon={<ArrowUpward />}
                                    onClick={loadOlder}
                                    data-start={rows.length - rows.findIndex((row) => !!row)}
                                >
                                    Load More
                                </Button>
                            </Box>
                        </Grid>
                    ) : null}
                    {rows.map((row, idx) =>
                        row ? (
                            <ChatRow
                                key={columns[0] ? `${row[columns[0]]}` : `id${idx}`}
                                senderId={senderId}
                                message={`${row[columns[1]]}`}
                                name={columns[2] ? `${row[columns[2]]}` : "Unknown"}
                                image={
                                    columns[3] && columns[3] != "_tp_index" && row[columns[3]]
                                        ? `${row[columns[3]]}`
                                        : undefined
                                }
                                className={className}
                                getAvatar={getAvatar}
                                index={idx}
                                showSender={showSender}
                                mode={mode}
                            />
                        ) : null
                    )}
                    <Box sx={anchorSx} ref={anchorDivRef} />
                </Grid>
                <Popper id={id} open={Boolean(anchorPopup)} anchorEl={anchorPopup} placement="right">
                    <Chip
                        label="A new message is available"
                        variant="outlined"
                        onClick={showBottom}
                        icon={<ArrowDownward />}
                    />
                </Popper>
                {withInput ? (
                    <>
                        {imagePreview && (
                            <Box mb={1}>
                                <Chip
                                    label={selectedFile?.name}
                                    avatar={<Avatar alt="Image preview" src={imagePreview} />}
                                    onDelete={handleImageDelete}
                                    variant="outlined"
                                />
                            </Box>
                        )}
                        <input
                            type="file"
                            ref={fileInputRef}
                            style={noDisplayStyle}
                            onChange={handleFileSelect}
                            accept="image/*"
                        />

                        <TextField
                            margin="dense"
                            fullWidth
                            onChange={onChangeHandler}
                            className={getSuffixedClassNames(className, "-input")}
                            label={`message (${senderId})`}
                            disabled={!active}
                            onKeyDown={handleAction}
                            slotProps={{
                                input: {
                                    startAdornment: allowSendImages ? (
                                        <InputAdornment position="start">
                                            <IconButton
                                                aria-label="upload image"
                                                onClick={handleAttachClick}
                                                edge="start"
                                                disabled={!active}
                                            >
                                                <AttachFile color={disableColor("primary", !active)} />
                                            </IconButton>
                                        </InputAdornment>
                                    ) : undefined,
                                    endAdornment: (
                                        <InputAdornment position="end">
                                            <IconButton
                                                aria-label="send message"
                                                onClick={handleClick}
                                                edge="end"
                                                disabled={!active || !(enableSend || imagePreview)}
                                            >
                                                <Send
                                                    color={disableColor(
                                                        "primary",
                                                        !active || !(enableSend || imagePreview)
                                                    )}
                                                />
                                            </IconButton>
                                        </InputAdornment>
                                    ),
                                },
                            }}
                            sx={inputSx}
                        />
                    </>
                ) : null}
                {props.children}
            </Paper>
        </Tooltip>
    );
};

export default Chat;
